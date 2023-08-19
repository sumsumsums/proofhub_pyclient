# Proofhub PyClient

Client to backup a ProofHub project using the ProofHub API V3. The API description is at https://github.com/ProofHub/api_v3 Note that the API description is not complete in some cases.

- It saves all objects as JSON on file system. Each object (groups, roles, projects) get a sub-directory. Projects have subdirectories for their respective subobjects, e.g. tasks, notebooks, ...

- Configuration is done with the configuration file (configuration.ini). You need the API Key of your ProofHub user.

- Deprecated objects not in your project anymore can be archive / moved to another directory.

- For files, it just downloads images for now. Download of other files is not possible with the API.

- It can be used in a batch job and tries not to download already downloaded files again.


Note that it is not tested much currently, so errors including dumps might happen.

# How to Run

Using python3 as environment.

1. Add API key and proofhub address to `configuration.ini`.
2. Configure what you want to download in `configuration.ini`
3. install requirements `pip install -r requirements.txt`
4. Run `python proofhub_client.py`

# Next Development

- download of other files beside images (maybe with a headless browser)

