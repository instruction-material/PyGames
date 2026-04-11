def transform(values: list[int]) -> list[int]:
	result: list[int] = []
	for value in values:
		result.append(value * 2 + 1)
	return result


def main() -> None:
	print(transform([3, 7, 11, 19]))


if __name__ == "__main__":
	main()
