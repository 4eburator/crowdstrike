import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.api.v1.nmap_api:app', port=5000, log_level='info')
