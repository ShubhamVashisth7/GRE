num_iterations=3
threads=(16 8 4 2 1) 
datasets=("libio")
index_techniques=("alexol")

for dataset in "${datasets[@]}"
do
    for thread_num in "${threads[@]}"
    do
        for index_technique in "${index_techniques[@]}"
        do
            for ((i=1; i<=$num_iterations; i++))
            do
                echo "iteration: $i, dataset: $dataset, thread_num: $thread_num, index_technique: $index_technique"
                ./build/microbench \
                --keys_file=./datasets/$dataset \
                --keys_file_type=binary \
                --read=1.0 --insert=0.0 \
                --init_table_ratio=1.0 \
                --table_size=20000000 \
                --operations_num=100000000 \
                --thread_num=$thread_num \
                --index=$index_technique \
                --memory
            done
        done
    done
done