from evaluation.tournament import print_tournament_result, run_tournament


def main() -> None:
    result = run_tournament(number_of_games=100, seed=42)
    print_tournament_result(result)


if __name__ == "__main__":
    main()
