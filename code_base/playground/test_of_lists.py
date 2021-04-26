


def main():
	
	list1 = [2,2]
	list2 = [2,2]

	new = set(list1+list2)
	print(new)

	bound = len(set(list1))+ len(set(list2))

	if len(new) == 2 and bound != 2: 
		print("collision")


main()