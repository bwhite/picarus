package picarus
import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"bytes"
	"errors"
	"mime/multipart"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"time"
)

type Conn struct {
	Email string
	ApiKey string
	LoginKey string
	Server string
}

func (conn *Conn) call(method string, path []string, params url.Values, files map[string][]byte, key string) ([]byte, error) {
	var err error
	var req *http.Request
	serverPrefix := conn.Server + "/" + strings.Join(path, "/")
	if method == "GET" {
		req, err = http.NewRequest(method, serverPrefix + "?" + params.Encode(), nil)
	} else {
		buf := new(bytes.Buffer)
		w := multipart.NewWriter(buf)
		for fileName, fileData := range files {
			_, err = w.CreateFormFile(fileName, fileName) // fw	
			if err != nil {
				return nil, err
			}
			buf.Write([]byte(fileData))
		}
		for name, values := range params {
			for _, value := range values {
				err = w.WriteField(name, value)
				if err != nil {
					return nil, err
				}
			}
		}
		w.Close()
		req, err = http.NewRequest(method, serverPrefix, buf)
		if err != nil {
			return nil, err
		}
		req.Header.Set("Content-Type", w.FormDataContentType())
	}
	if err != nil {
		return nil, err
	}
	req.SetBasicAuth(conn.Email, key)
	response, err := http.DefaultClient.Do(req) // res
	if err != nil {
		return nil, err
	}
	body, err := ioutil.ReadAll(response.Body)
	defer response.Body.Close()
	if err != nil {
		return nil, err
	}
	if response.StatusCode != 200 {
		return nil, errors.New(fmt.Sprintf("Bad status[%d][%s]", response.StatusCode, body))
	}
	return body, nil
}

func decodeLod(values []map[string]string) ([]map[string]string, error) {
	out := []map[string]string{}
	for _, value := range values {
		curOut, err := decodeDict(value)
		if err != nil {
			return nil, err
		}
		out = append(out, curOut)
	}
	return out, nil
}

func decodeDict(value map[string]string) (map[string]string, error) {
	out := map[string]string{}
	for k, v := range value {
		// TODO: Use a checked version of b64dec
		if k == "row" {
			out[k] = B64Dec(v)
		} else {
			out[B64Dec(k)] = B64Dec(v)
		}
	}
	return out, nil
}

func decodeValues(value map[string]string) (map[string]string, error) {
	out := map[string]string{}
	for k, v := range value {
		// TODO: Use a checked version of b64dec
		out[k] = B64Dec(v)
	}
	return out, nil
}

func encodeDict(value map[string]string) map[string]string {
	out := map[string]string{}
	for k, v := range value {
		out[B64Enc(k)] = B64Enc(v)
	}
	return out
}

func encodeValues(value map[string]string) map[string]string {
	out := map[string]string{}
	for k, v := range value {
		out[k] = B64Enc(v)
	}
	return out
}

func encodeFiles(files map[string][]byte) map[string][]byte {
	out := map[string][]byte{}
	for k, v := range files {
		out[B64Enc(k)] = v
	}
	return out
}

func (conn *Conn) GetRow(table string, row string, columns []string) (map[string]string, error) {
	params := url.Values{}
	if len(columns) > 0 {
		params.Set("columns", encodeColumns(columns))
	}
	data, err := conn.call("GET", []string{"v0", "data", table, UB64Enc(row)}, params, map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeDict(dataParsed)
}

func (conn *Conn) GetTable(table string, columns []string) ([]map[string]string, error) {
	params := url.Values{}
	if len(columns) > 0 {
		params.Set("columns", encodeColumns(columns))
	}
	data, err := conn.call("GET", []string{"v0", "data", table}, params, map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := []map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeLod(dataParsed)
}

func encodeColumns(columns []string) string {
	columnsB64 := []string{}
	for _, c := range columns {
		columnsB64 = append(columnsB64, B64Enc(c))
	}
	return strings.Join(columnsB64, ",")
}


func (conn *Conn) GetSlice(table string, startRow string, stopRow string, columns []string, params map[string]string) ([]map[string]string, error) {
	if len(columns) > 0 {
		params["columns"] = encodeColumns(columns)
	}
	data, err := conn.call("GET", []string{"v0", "slice", table, UB64Enc(startRow), UB64Enc(stopRow)}, mapToUrlValues(params), map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := []map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeLod(dataParsed)
}


type ScannerState struct {
	startRow, stopRow string
	prevData *[]map[string]string
	nextRow int
	columns []string
	params map[string]string
	conn *Conn
	Done bool
}

func (conn *Conn) Scanner(table string, startRow string, stopRow string, columns []string, params map[string]string) *ScannerState {
	return &ScannerState{startRow: startRow, stopRow: stopRow, nextRow: 0, columns: columns, params: params, Done: false}
}

func (ss *ScannerState) Next() (string, map[string]string, error) {
	if ss.Done {
		return "", nil, nil
	}
	if ss.prevData == nil || (ss.prevData != nil && len(*ss.prevData) == ss.nextRow) {
		var startRow string
		var excludeStart string
		if ss.prevData == nil {
			excludeStart = "0"
			startRow = ss.startRow
		} else {
			excludeStart = "1"
			startRow = (*ss.prevData)[ss.nextRow - 1]["row"]
		}
		ss.params["excludeStart"] = excludeStart
		data, err := ss.conn.GetSlice("images", startRow, ss.stopRow, ss.columns, ss.params)
		if err != nil {
			return "", nil, err
		}
		if len(data) == 0 {
			ss.Done = true
			return "", nil, nil
		}
		ss.prevData = &data
		ss.nextRow = 0
	}
	columns := (*ss.prevData)[ss.nextRow]
	row := columns["row"]
	delete(columns, "row")
	ss.nextRow += 1
	return row, columns, nil
}

func mapToUrlValues(data map[string]string) url.Values {
	out := url.Values{}
	for k, v := range data {
		out.Set(k, v)
	}
	return out
}

func (conn *Conn) PostSlice(table string, startRow string, stopRow string, params map[string]string) (map[string]string, error) {
	data, err := conn.call("POST", []string{"v0", "slice", table, UB64Enc(startRow), UB64Enc(stopRow)}, mapToUrlValues(encodeValues(params)), map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeDict(dataParsed)
}

type Slice struct {
    StartRow, StopRow string
}

func encodeSlices(slices []Slice) string {
	out := []string{}
	for _, v := range slices {
		out = append(out, B64Enc(v.StartRow) + "," + B64Enc(v.StopRow))
	}
	return strings.Join(out, ";")
}

func (conn *Conn) PostTable(table string, params map[string]string, files map[string][]byte, slices []Slice) (map[string]string, error) {
	if len(slices) > 0 {
		params["slices"] = encodeSlices(slices)
	}
	data, err := conn.call("POST", []string{"v0", "data", table}, mapToUrlValues(encodeDict(params)), encodeFiles(files), conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeValues(dataParsed)
}

func (conn *Conn) PostRow(table string, row string, params map[string]string) (map[string]string, error) {
	data, err := conn.call("POST", []string{"v0", "data", table, UB64Enc(row)}, mapToUrlValues(encodeValues(params)), map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeDict(dataParsed)
}

func (conn *Conn) PatchRow(table string, row string, params map[string]string, files map[string][]byte) (map[string]string, error) {
	data, err := conn.call("PATCH", []string{"v0", "data", table, UB64Enc(row)}, mapToUrlValues(encodeDict(params)), encodeFiles(files), conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeDict(dataParsed)
}

func UB64Dec(s string) string {
	decoded, err := base64.URLEncoding.DecodeString(s)
	if err != nil {
		panic(err)
	}
	return string(decoded)
}

func B64Dec(s string) string {
	decoded, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		fmt.Println(s)
		panic(err)
	}
	return string(decoded)
}

func B64DecBytes(s string) []byte {
	decoded, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		fmt.Println(s)
		panic(err)
	}
	return decoded
}


func UB64Enc(s string) string {
	return base64.URLEncoding.EncodeToString([]byte(s))
}

func B64Enc(s string) string {
	return base64.StdEncoding.EncodeToString([]byte(s))
}

func (conn *Conn) WatchJob(row string) (map[string]string, error) {
	for {
		data, err := conn.GetRow("jobs", row, []string{})
		if err != nil {
			return nil, err
		}
		fmt.Println(data)
		if data["status"] == "completed" {
			return data, nil
		}
		time.Sleep(1000 * time.Millisecond)
	}
}