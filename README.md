# Diary_Python_01
Today, I wanna write my code in learning python, wwwwwwwww this is actualy beautiful language conding, i like it

2025 1031 Fri

record my studying in Git, hoping someone find them and have a smile to my poor code

AI influence our coding a lot, I also ues them to help me to learn, which is a better way to a function? I will use it and memory code to grow

Thanks for watching owo

2025 1103 Mon

I'm back in the Monday, I've not upgrade my code in 1101 Saturday.

I was just using "class" and "__main__" in python for the first time, I will share 2rd part of my code continuously, hope for you watching.

Key words:

    self.connection = pymysql.connect(**self.config)

    with self.connection.cursor() as cursor:

        cursor.execute("SELECT kg_id, kg_code FROM xj_kg_space_info_tb WHERE kg_name = %s", (kg_name,))
    
        kg_query_result = cursor.fetchall()  # kg query resutl
    
(I will add the "Key words" part for my memory in learning python, wwwwww)

2025 1104 Tues

The code in 3rd day was definitely easiest part. Maybe tomorrow we can finish the test python.

Key words:

    for i, kg_result in enumerate(kg_results, start=1):
    
    result_dict["total_time"] = round(time.time() - total_start_time, 3)

Thanks for watching~

2025 1105 Wends

The "with as" is the most funny part last month in my coding learning, so that I memory it deepest whenever it comes.

and so this is the last day to practice the Multi-auto-test script, thank for your watching.

Key words:

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
		future = executor.submit(db_test._process_single_kg, kg_name)

    avg_total_time = round(sum(res["total_time"] for res in test_results) / len(test_results), 3) if test_results else 0

    if __name__ == "__main__":

next code we will see, see you (^///^)

2025 1106 Thur

Maybe, you find your D Drive full, like me. 

I want a code can help list all directory I wanted to look at how big it is, rather than right-licking every dir to check its property. 

So I designed it (^///^) practice1106_en.py

2025 1107 Fri practice1107_en.py

In this simple terms, the code wil traverse all files in folder, copy and maintain the original folder structure.

That code is so simple that i have the sensation that i did it ! (^///^) even though ai help me a lot, i can control the code and write it again afterwards by myself only.

2025 1115 Satur text_jinhao01.py

I stayed at home for a week and didn't go to the office, because I had a cold that is really uncomfortable. I was extremely sleepy. 

Today is Saturdat. I promise a friend, who haven't use any python coding utility, to package the code "step06douyin.py" for downloading videos for him. 

For the reason that some video websites have watermarks on the downloaded videos or they simply cannot be downloaded, I did this for douyin platform. 

Of course, I also utilized the help of AI. I will learn it! Hope that the next time I can write it all by myself.

Key words:

(code about "os.path" for reviewign)

2025 1118 Tues

I used config.py to save all the variables as GLOBAL. So that could be easy to control what I want to change.

Today is my brithday. And I learnt a lot in os library. But it's pity that company's code was to MinIO. So tomorrow I'd learn it to enrich my code.

Key words:

	None
	
2025 1119 Wed text_jinhao01_en.py test_jinhao_config_en.py

Today I aim to master minIO library, so I did it ヾ(≧▽≦*)o

Key words:

	objects = minio_client.list_objects(bucket_name, prefix=test_folder, recursive=True)
	
	file_path = obj.object_name
	file_ext = os.path.splitext(file_path)[1].lower()

	stat = minio_client.stat_object(bucket_name, file_path)
