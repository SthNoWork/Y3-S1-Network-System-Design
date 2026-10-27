import socket,sys
proto,role=sys.argv[1:3]
if proto not in ('tcp','udp') or role not in ('server','client'):
    raise SystemExit('Use: echo.py tcp|udp server|client [message]')
kind=socket.SOCK_STREAM if proto=='tcp' else socket.SOCK_DGRAM
with socket.socket(socket.AF_INET,kind) as s:
    if role=='server':
        s.bind(('127.0.0.1',12000)); print(proto,'server on loopback port 12000; Ctrl+C to stop')
        if proto=='tcp':
            s.listen(1)
            while True:
                c,addr=s.accept()
                with c:
                    c.settimeout(5); data=b''
                    try:
                        while b'\n' not in data and len(data)<4096:
                            part=c.recv(min(1024,4096-len(data)))
                            if not part: break
                            data+=part
                        c.sendall(data)
                    except socket.timeout: print('Client read timeout')
        else:
            while True:
                data,addr=s.recvfrom(4096);s.sendto(data,addr)
    else:
        s.settimeout(2);data=(' '.join(sys.argv[3:]) or 'hello class').encode()+b'\n'
        if len(data)>4096:raise SystemExit('Use a message shorter than 4096 bytes')
        print('Target:',('127.0.0.1',12000))
        try:
            if proto=='tcp':
                s.connect(('127.0.0.1',12000)); print('Local endpoint:',s.getsockname());s.sendall(data);reply=b''
                while b'\n' not in reply and len(reply)<4096:
                    part=s.recv(4096-len(reply))
                    if not part: break
                    reply+=part
            else:
                s.sendto(data,('127.0.0.1',12000)); print('Local endpoint:',s.getsockname());reply,peer=s.recvfrom(4096)
            print('Reply:',reply.decode(errors='replace').rstrip())
        except (socket.timeout,ConnectionError,OSError) as e:print(type(e).__name__+':',e)
