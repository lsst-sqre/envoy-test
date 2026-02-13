# Adapted from the nodejs server here:
# https://raw.githubusercontent.com/envoyproxy/gateway/latest/examples/kubernetes/ext-auth-http-service.yaml
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKENS = {
    "token1": "user1",
    "token2": "user2",
    "token3": "user3",
}


class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"url: {self.path}")

        authorization = self.headers.get("Authorization", "")
        extracted = authorization.split(" ")

        if len(extracted) == 2 and extracted[0] == "Bearer":
            token = extracted[1]
            user = TOKENS.get(token)
            print(f'token: "{token}" user: "{user}"')
            if user is not None:
                # Successful auth
                self.send_response(200)
                self.send_header("x-current-user", user)
                self.end_headers()
                return

        # Unauthorized
        self.send_response(401)
        self.send_header("x-added-deny-header", "bar")
        self.send_header("x-requested-auth-url", self.path)
        self.end_headers()
        self.wfile.write(b"Nope!")


def main():
    port = int(os.environ.get("PORT", "9002"))
    server = HTTPServer(("", port), AuthHandler)
    print(f"starting HTTP server on: {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
