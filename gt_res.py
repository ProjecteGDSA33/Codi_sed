import pandas as pd


gt = pd.read_csv('C:\Users\IRENE\Downloads\sed2013_task2_dataset_train_gs.csv',sep='\t')
result = pd.read_csv('C:\Users\IRENE\Resultats.csv',sep=' ')

text_gt_res = open("GT_RES.txt", "w")
text_gt_res.write("document_id event_type\n")

for id_res in result.document_id:
    id_gt=0
    while (id_gt < len(gt)):
        if(id_res == gt.document_id[id_gt]):
            text_gt_res.write( str(id_res)+" "+str(gt.event_type[id_gt]))
            text_gt_res.write("\n")
        id_gt=id_gt+1

text_gt_res.close()
