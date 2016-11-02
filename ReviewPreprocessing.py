import glob
import sys
reload(sys)


i=0;
with open ('C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\Benchmark Dataset\Canon G3.txt', 'rt') as in_file:
	
	for line in in_file:
		file1 =open("C:\Users\Vinod Chhapariya\Desktop\TDBMS\Project\CanonG3\Review_" + str(i) + ".txt",'a')
	

		if line.startswith('[t]') :
			print str(line)
			i+=1

		else:
			file1.write(str(line))
	
		
		
		  
  		
  		
        
  

