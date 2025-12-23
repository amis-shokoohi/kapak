# Changelog

# [4.0.1]

### Fixed

- Check reserved bytes in file header and show better error message while decrypting ([1fe7178](https://github.com/amis-shokoohi/kapak/commit/1fe71782a189177288e59f0d803925bddc6181b1))

### Changed

- Updated dependencies to latest versions ([feada0c](https://github.com/amis-shokoohi/kapak/commit/feada0c2c454d650ac34bbaa69e899b5acdb3f49))
- Minimum officially supported version is now Python 3.10

## [4.0.0]

### Changed

- Bumped cryptography from 39.0.0 to 39.0.1

## [4.0.0-rc.2]

### Added

- Added more test coverage

### Fixed

- Fixed issue with padding

## [4.0.0-rc.1]

### Added

- Added stdin/stdout support for cli
- Read password from user specified file
- Added more tests

### Changed

- Used `cryptography v39.0.0`
- Changed header format of encrypted file
- Changed key verification algorithm

### Removed

- Removed password length limit
- Removed folder encryption
- Removed folder zip compression
