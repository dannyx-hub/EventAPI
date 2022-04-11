def changename(template,name,start,stop,descr):
	with open(template,"r") as htmlfile:
		checkfile = htmlfile.read()
		for line in checkfile:
			strfile = str(checkfile)
		msg = strfile.format(name,start,stop,descr)
		return msg

#print(strfile.replace("{{name}}","dupadupa123.")
det=changename("template.html","test2","2022-03-03","2022-03-04","opis dojebany w kosmos")
print(det)
