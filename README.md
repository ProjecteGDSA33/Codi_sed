1. Read train images in folder. 
2. Obtain the metadata.
3. Create a file with the format event_type + #tags of each type of image.

Do the 3 first steps executing the file: super_vector.py
After the execution you will obtain a file named supervector.txt and a supervector_svm.txt
The second one contain a supervector tfidf for each class.

4. With the codi_tfidf.py we can read the supervector.txt file and the test images in a folder. It shows the answer values in the Results.txt file.

5. To evaluate this, use the eval.py script. Execute this file with the command below: 
   %run [directory path] --baseline --challenge2 [Ground_truth_file] [Own_results_file]
 
