from distributed import Client, LocalCluster
from .cli import build_parser
from .etl import run_pipeline

def main():

    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "local":
        cluster = LocalCluster(
            n_workers=args.n_workers,
            threads_per_worker=args.threads_per_worker
        )
        client = Client(cluster)
        print("LocalCluster gestartet:", cluster.dashboard_link)

    else:
        client = Client(args.scheduler_address)
        print("Verbunden mit Scheduler:", args.scheduler_address)

    run_pipeline(args.input, args.output)

    client.close()

if __name__ == "__main__":
    main()