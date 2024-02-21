import subprocess
import time

start_time = time.time()

print("Renaming")
subprocess.run("python renaming.py", shell=True)
print("Finished renaming")

print("Parsing...")
subprocess.run("python parser.py", shell=True)
print("Finished parsing")

print("Removing duplicates...")
subprocess.run("python remove_dup.py", shell=True)
print("Finished removing duplicates")

print("Tokenizing...")
subprocess.run("python tokenizer.py", shell=True)
print("Finished tokenizing")

print("Starting count_line.py ...")
subprocess.run("python count_line.py", shell=True)

print("Detecting clones...")
subprocess.run("python clone_detector.py", shell=True)
print("Finished detecting clone")

print("Merging csv files for complete individual file statistics...")
subprocess.run("python csv_merging.py", shell=True)
print("Finished merging")


#files for visulization (the order is not required to be fixed)

print("Running Visulization")

print("Starting clone_line_count.py ...")
subprocess.run("python clone_line_count.py", shell=True)

print("Starting clone%_graph.py ...")
subprocess.run("python clone%_graph.py", shell=True)

print("Starting clone_type_pie.py ...")
subprocess.run("python clone_type_pie.py", shell=True)

print("Starting clone_type_pie_no_ty5.py ...")
subprocess.run("python clone_type_pie_no_ty5.py", shell=True)

print("Starting indi_clone_types.py ...")
subprocess.run("python indi_clone_types.py", shell=True)

print("Starting indi_clone_types_no_ty5.py ...")
subprocess.run("python indi_clone_types_no_ty5.py", shell=True)


end_time = time.time()
execution_time = end_time - start_time
print(f"Well done, the total execution time is {execution_time} seconds")

