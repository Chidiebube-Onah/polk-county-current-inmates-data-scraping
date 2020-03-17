import csv
from multiprocessing.dummy import Pool as ThreadPool 
def create_csv(filename):
    with open (filename,'w') as file:
        writer=csv.writer(file)
        writer.writerow(["Offender/Name ID", "Name", "Book Date",
         "City", "Holding Location", "Age", "Height", "Weight",
          "Race", "Sex:", "Eyes", "Hair", "Img_Src"])


def write_csv(filename, dataset):
    with open (filename,'a+') as file:
        writer=csv.writer(file)

        def _write_row(row):
            writer.writerow(row)

        pool = ThreadPool(9)
        pool.map(_write_row, dataset)
        pool.close()
        pool.join()
        print("{0} dataset(s) written to csv".format(len(dataset)), end=" ")