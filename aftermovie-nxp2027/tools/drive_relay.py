#!/usr/bin/env python3
"""Relay HTTP local -> Google Drive (respeita HTTPS_PROXY/CA do ambiente), com suporte a Range.
O ffmpeg estático não fala TLS via proxy; ele lê http://127.0.0.1:8765/<file_id>."""
import http.server, socketserver, requests, os

CA = "/root/.ccr/ca-bundle.crt"
U = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"
sess = requests.Session(); sess.verify = CA if os.path.exists(CA) else True

class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass
    def _go(self, head=False):
        fid = self.path.strip("/").split("?")[0]
        hdr = {}
        if "Range" in self.headers: hdr["Range"] = self.headers["Range"]
        import time
        r = None
        for attempt in range(3):  # cota anônima do Drive: espera e tenta de novo
            try:
                r = sess.get(U.format(fid), headers=hdr, stream=True, timeout=60)
            except Exception as e:
                r = None; time.sleep(10); continue
            if "text/html" in r.headers.get("Content-Type", ""):
                r.close(); r = None
                open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quota.log'), "a").write(f"{time.time():.0f} {fid} quota attempt {attempt}\n")
                time.sleep(20 * (attempt + 1)); continue
            break
        if r is None:
            self.send_error(503, "drive quota"); return
        self.send_response(r.status_code)
        for k in ("Content-Type", "Content-Length", "Content-Range", "Accept-Ranges"):
            if k in r.headers: self.send_header(k, r.headers[k])
        if "Accept-Ranges" not in r.headers: self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        if head: r.close(); return
        try:
            for chunk in r.iter_content(1 << 16):
                self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            r.close()
    def do_GET(self): self._go()
    def do_HEAD(self): self._go(True)

class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True; allow_reuse_address = True

S(("127.0.0.1", 8765), H).serve_forever()
