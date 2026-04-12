import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Watchlist für Aktien und ETFs",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
    )

    parser.add_argument("file", type=str, help="Pfad zur Datei mit den Portfoliodaten")
    parser.add_argument("-z", type=int, default=10, help="Zeithorizont in Jahren")
    parser.add_argument("-r", type=str, default="gering", choices=['gering', 'mittel', 'hoch'], help="Risikoprofil")

    args = parser.parse_args()
    
    print(f"Datei: {args.file}")
    print(f"Zeithorizont: {args.z} Jahre")
    print(f"Risikoprofil: {args.r}")
