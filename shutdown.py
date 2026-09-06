def fshutdown(server):
    print("\nShutting down server...")
    server.shutdown()
    server.server_close()
    print("Server stopped.")