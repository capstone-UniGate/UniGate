# Frontend E2E Testing Setup Guide

This guide provides instructions for setting up and running end-to-end (E2E) tests for your frontend project using `just` for command automation. It includes steps for both Linux and Windows environments.

---

## Prerequisites

Refer to the official [just documentation](https://just.systems/man/en/prerequisites.html) for prerequisites and ensure `just` is installed on your system.

---

## E2E Testing Setup

The E2E setup is complete, and test cases can be found in the `frontend/tests/test_cases` directory.

### Running Tests with `just`

1. **Open a terminal**:

   - Start the frontend development server by running:
     ```bash
     just frontend-dev
     ```

2. **In a second terminal**:
   - Run the E2E tests:
     ```bash
     just frontend-test
     ```

### Running Without `just`

If you aren’t using `just`, follow these manual steps:

1. **Sync dependencies**: Run the command `uv` inside the `frontend` folder to sync dependencies.
2. **Activate virtual environment**: Enable the virtual environment located in the `frontend` folder.
3. **Run tests**: Use `pytest` to execute the tests:
   ```bash
   pytest tests/
   ```

---

## Installing `just` on Linux

For Linux users, if the `just` package isn’t available in your package manager, install it with `cargo`:

```bash
cargo install just
```

---

## Installing `just` on Windows

1. **Set Execution Policy**:

   - Run PowerShell as an administrator and execute the following:
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

2. **Install Scoop** (if needed):

   - Install `scoop` to help manage Windows installations:
     ```powershell
     irm get.scoop.sh | iex
     ```

3. **Install `just` via Scoop**:

   - After installing `scoop`, install `just`:
     ```powershell
     scoop install just
     ```

4. **Configure Git for Windows (recommended)**:
   - Install Git for Windows to access a Unix-like command line, or use PowerShell as follows.

### Running `just` with PowerShell on Windows

To use `just` with PowerShell instead of Git Bash:

1. **Edit the `justfile`**:

   - Add this line to set the shell to PowerShell:
     ```just
     set shell := ["powershell", "-Command"]
     ```

2. **Modify syntax**:

   - Replace all occurrences of `&&` in the `justfile` with `;` for compatibility.

3. **Run Commands**:
   - Use `just.exe` instead of `just` to execute commands, e.g., `just.exe frontend-dev`.

---

## Browser Compatibility

The E2E tests are compatible only with Chromium-based browsers (such as Chrome, Brave, and Opera).

---

This setup should help you run your frontend tests smoothly across different environments.
