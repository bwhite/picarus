package picarus
import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"bytes"
	"mime/multipart"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"time"
)

type PostRowResponse struct {
	Row string `json:"row"`
}

type PicarusConn struct {
	Email string
	ApiKey string
	LoginKey string
	Server string
}

func (conn *PicarusConn) call(method string, path []string, params url.Values, files map[string][]byte, key string) ([]byte, error) {
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
	defer response.Body.Close()
	return ioutil.ReadAll(response.Body)
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


func (conn *PicarusConn) GetRow(table string, row string, columns []string) (map[string]string, error) {
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

func (conn *PicarusConn) GetTable(table string, columns []string) ([]map[string]string, error) {
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


func (conn *PicarusConn) GetSlice(table string, startRow string, stopRow string, columns []string) ([]map[string]string, error) {
	params := url.Values{}
	if len(columns) > 0 {
		params.Set("columns", encodeColumns(columns))
	}
	data, err := conn.call("GET", []string{"v0", "slice", table, UB64Enc(startRow), UB64Enc(stopRow)}, params, map[string][]byte{}, conn.ApiKey)
	if err != nil {
		return nil, err
	}
	dataParsed := []map[string]string{}
	json.Unmarshal(data, &dataParsed)
	return decodeLod(dataParsed)
}

func mapToUrlValues(data map[string]string) url.Values {
	out := url.Values{}
	for k, v := range data {
		out.Set(k, v)
	}
	return out
}

func (conn *PicarusConn) PostSlice(table string, startRow string, stopRow string, params map[string]string) (map[string]string, error) {
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

func (conn *PicarusConn) PostTable(table string, params map[string]string, files map[string][]byte, slices []Slice) (map[string]string, error) {
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

func (conn *PicarusConn) WatchJob(row string) error {
	for {
		data, err := conn.GetRow("jobs", row, []string{})
		if err != nil {
			return err
		}
		fmt.Println(data)
		if data["status"] == "completed" {
			return nil
		}
		time.Sleep(1000 * time.Millisecond)
	}
}