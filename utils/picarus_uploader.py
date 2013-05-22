import argparse
import picarus
import glob
import base64
import os


def main(email, table, prefix, path, picarus_server, api_key=None, login_key=None, otp=None, start_row=''):
    path = os.path.abspath(path)
    if otp:
        api_key = picarus.PicarusClient(email=email, login_key=login_key, server=picarus_server).auth_yubikey(otp)['apiKey']
    if api_key is None:
        raise ValueError('api_key or login_key/otp must be set!')
    if start_row:
        start_row = base64.urlsafe_b64decode(start_row)
    client = picarus.PicarusClient(email=email, api_key=api_key, server=picarus_server)
    for row_path in sorted(glob.glob(path + '/*')):
        row = prefix + base64.urlsafe_b64decode(os.path.basename(row_path))
        if row < start_row:
            continue
        columns = {}
        for column_path in glob.glob(row_path + '/*'):
            column = base64.urlsafe_b64decode(os.path.basename(column_path))
            columns[column] = open(column_path, 'rb').read()
        print('Sending [%r] ub64:[%s] to Picarus' % (row, base64.urlsafe_b64encode(row)))
        client.patch_row(table, row, columns)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Picarus bulk directory uploader.  Path points to a directory encoded as <path>/<ub64row>/<ub64col> for each column, with the file contents the binary column value (not encoded).  ub64 refers to urlsafe b64 encoding.  Rows uploaded in ascending lexical order.')
    parser.add_argument('email')
    parser.add_argument('table', choices=['images'])
    parser.add_argument('prefix', help='Prefix added to each row (plaintext, not encoded)')
    parser.add_argument('path', help='Local path to the directory to upload')
    parser.add_argument('--start_row', help='Skip all rows before this, must include prefix and be ub64 encoded (useful for resuming, paste failed row here)')
    parser.add_argument('--api_key')
    parser.add_argument('--login_key')
    parser.add_argument('--otp')
    parser.add_argument('--picarus_server', default='https://api.picar.us')
    main(**vars(parser.parse_args()))
