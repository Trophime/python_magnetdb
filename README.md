# MagnetDB

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lncmi control and monitoring website**.
See `python_magnetrun` for more details

## Development setup

1. Install python dependencies:
    ```shell
    pip3 install -r requirements.txt
    ```

2. Start dependencies with docker:
    ```shell
    docker-compose up
    ```

3. Setup Minio bucket:
   1. Sign in to http://localhost:9080/ with minio/minio123
   2. Create bucket on http://localhost:9080/add-bucket

4. Run migrations:
    ```shell
    orator migrate -c config.py
    ```

5. Configure LemonLDAP (https://github.com/LemonLDAPNG/lemonldap-ng-docker):
   1. Sign in to http://auth.example.com/ with dwho/dwho
   2. Enable OpenID Connect in Administration > WebSSO Manager > General Parameters > Issuer modules > OpenID Connect
   3. Create OpenID relying party in Administration > WebSSO Manager > OpenID Connect Relying Parties > Add OpenID Relying Party
   4. Go in Administration > WebSSO Manager > OpenID Connect Relying Parties > "Name of the relying party" > Options > Basic
   5. Set Client ID to `testid`
   6. Set Client secret to `testsecret`
   7. Set Allowed redirection addresses for login to `http://localhost:8080/sign_in`

6. Setup front-end:
   ```shell
    cd web
    yarn install
    ```

7. Run seeds:
   ```shell
   python3 -m python_magnetdb.seeds
   ```

8. Start front-end:
   ```shell
   cd web
   export API_ENDPOINT=http://localhost:8000
   yarn serve
   ```

9. Start back-end:
   ```shell
   export S3_ENDPOINT=localhost:9000 S3_ACCESS_KEY=minio S3_SECRET_KEY=minio123 S3_BUCKET=magnetdb
   uvicorn python_magnetdb.main:app --reload --log-level=debug
   ```
