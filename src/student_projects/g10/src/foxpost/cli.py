import argparse

def build_parser():
    p = argparse.ArgumentParser("FoxPost Pipeline")

    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)

    p.add_argument("--mode", choices=["local","cluster"], default="local")
    p.add_argument("--scheduler-address")

    p.add_argument("--n-workers", type=int, default=2)
    p.add_argument("--threads-per-worker", type=int, default=1)

    return p