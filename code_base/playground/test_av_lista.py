



def main():

	dict = {}

	dict[1] = 2

	dict[3] = 0.3

	for i in range(5):
		if i not in dict:
				dict[i] = 1

	print(dict)

	

main()