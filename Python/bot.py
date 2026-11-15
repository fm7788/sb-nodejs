#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 极简部署脚本（仅用标准库，execv 替换进程以释放 Python 占用）
# 专为超低内存设备，输出仅 insecure=1 节点

import os
import sys
import platform
import stat
import subprocess
import urllib.request

# ---------- 配置 ----------
HYSTERIA_VERSION = "v2.6.2"
SERVER_PORT = 5000       # 端口这里填你面板的端口
AUTH_PASSWORD = "abc123" # 建议换复杂点
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
RETRIES = 2
# --------------------------

def arch_name():
    m = platform.machine().lower()
    if "aarch64" in m or "arm64" in m:
        return "arm64"
    if "x86_64" in m or "amd64" in m:
        return "amd64"
    return None

def download_binary(dest):
    arch = arch_name()
    if not arch:
        print("❌ 无法识别 CPU 架构:", platform.machine())
        sys.exit(1)
    bin_name = f"hysteria-linux-{arch}"
    if os.path.exists(dest):
        print("✅ 二进制已存在，跳过下载。")
        return

    url = f"https://github.com/apernet/hysteria/releases/download/app/{HYSTERIA_VERSION}/{bin_name}"
    print("⏳ 下载:", url)
    last_exc = None
    for i in range(RETRIES+1):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                if resp.status >= 400:
                    raise Exception("HTTP status %s" % resp.status)
                with open(dest, "wb") as f:
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IXUSR)
            print("✅ 下载完成并设置可执行:", dest)
            return
        except Exception as e:
            last_exc = e
            print("下载失败，重试:", i, "err:", e)
    print("❌ 下载失败，最后错误:", last_exc)
    sys.exit(1)

def ensure_cert():
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        print("✅ 发现证书，使用现有 cert/key。")
        return
    print("🔑 未发现证书，尝试使用 openssl 生成自签 ECDSA 证书...")
    cmd = [
        "openssl", "req", "-x509", "-nodes",
        "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:prime256v1",
        "-days", "3650",
        "-keyout", KEY_FILE,
        "-out", CERT_FILE,
        "-subj", "/CN=localhost"
    ]
    try:
        ret = subprocess.run(cmd)
        if ret.returncode != 0:
            raise Exception("openssl 返回非零状态")
        print("✅ 证书生成成功。")
    except FileNotFoundError:
        print("❌ 未找到 openssl，可考虑在其它机器生成证书并拷贝到设备。")
        sys.exit(1)
    except Exception as e:
        print("❌ 证书生成失败:", e)
        sys.exit(1)

def write_config():
    cfg = f"""listen: ":{SERVER_PORT}"
tls:
  cert: "{os.path.abspath(CERT_FILE)}"
  key: "{os.path.abspath(KEY_FILE)}"
auth:
  type: "password"
  password: "{AUTH_PASSWORD}"
bandwidth:
  up: "250mbps"
  down: "250mbps"
quic:
  max_idle_timeout: "10s"
  max_concurrent_streams: 4
  initial_stream_receive_window: 65536
  max_stream_receive_window: 131072
  initial_conn_receive_window: 131072
  max_conn_receive_window: 262144
"""
    with open("server.yaml", "w") as f:
        f.write(cfg)
    print("✅ 写入配置 server.yaml（极小化）。")

def get_public_ip():
    urls = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://ipv4.icanhazip.com",
    ]
    for u in urls:
        try:
            with urllib.request.urlopen(u, timeout=5) as resp:
                ip = resp.read().decode().strip()
                if ip and "." in ip:
                    print(f"🌐 自动获取公网 IP: {ip}")
                    return ip
        except Exception:
            continue
    print("❌ 获取公网 IP 失败，请手动设置")
    sys.exit(1)

def output_uri(pub_ip):
    base = f"{AUTH_PASSWORD}@{pub_ip}:{SERVER_PORT}"
    uri_insecure = f"hysteria2://{base}?insecure=1#Hy2-Insecure"

    print("\n=== ✅ 节点链接已生成 ===")
    print(uri_insecure)
    print("============================================\n")

def main():
    print("🚀 极简部署启动（标准库版，仅 insecure 节点）")
    arch = arch_name()
    if not arch:
        print("❌ 无法识别架构，退出。")
        sys.exit(1)

    bin_file = f"hysteria-linux-{arch}"
    download_binary(bin_file)
    ensure_cert()
    write_config()

    pub_ip = get_public_ip()
    output_uri(pub_ip)

    argv = [os.path.abspath(f"./{bin_file}"), "server", "-c", "server.yaml"]
    print("🚀 用 execv 启动 hysteria（进程将被替换）:", " ".join(argv))
    try:
        os.execv(argv[0], argv)
    except Exception as e:
        print("❌ execv 启动失败:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
