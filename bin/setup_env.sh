python3 -m venv .rs
activate() {
    . .rs/bin/activate
    echo "installing requirements to virtual environment"
    pip install -r requirements.txt
}
activate
