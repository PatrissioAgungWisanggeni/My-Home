from django.shortcuts import render, get_object_or_404, redirect
from random import sample
from .models import CoffeeShop, Riwayat, Favorite
from math import radians, sin, cos, sqrt, atan2
import numpy as np


def home(request):
    return render(request, 'skripsi/Home.html')


def beranda(request):
    
    all_data = CoffeeShop.objects.all()
    datas = sample(list(all_data), min(6, len(all_data)))

    context = {
        'datas': datas,
    }

    return render(request, 'skripsi/Beranda.html', context)


def search(request):
    cari = request.GET.get('cari')
    
    tetangga = request.POST.get('k')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    print("Nilai latitude:", latitude)
    print("Nilai longitude:", longitude)
    print("Jumlah tetangga:", tetangga)

    all_data = CoffeeShop.objects.all()
    data_favorite = Favorite.objects.values_list('coffee_shop_id', flat=True)
    
    datas = []
    all_riwayat = []
    neighbors = []
    data_terdekat = []

    if cari: # mencari beredasarkan query nama
        datas = CoffeeShop.objects.filter(nama__istartswith=cari)
    else:
        datas = sample(list(all_data), (min(6, len(all_data))))
        all_riwayat = Riwayat.objects.all().order_by('-waktu_pemilihan')[:10]

        if latitude is not None and longitude is not None: # mencari berdasarkan lokasi pengguna saat ini (latitude dan longitude)
            # mengambil kolom latitude dan longitude dari dataset
            distance = CoffeeShop.objects.values('latitude', 'longitude')
            jarak = []
            
            # konversi menjadi bertipe float
            for row in distance:
                lat_ke_i = float(row['latitude'])
                long_ke_i = float(row['longitude'])
                jarak.append((lat_ke_i, long_ke_i))

            # konversi data input pengguna menjadi float 
            lat = float(latitude)
            long = float(longitude)
            k = int(tetangga)
            data_test = lat, long
            neighbors = get_neighbors(jarak, data_test, k) # menjalankan get_neighbors agar bisa memperoleh tetangga terdekatnya

            for x in neighbors: # berfungsi agar jarak dapat diakses di html
                x_tetangga = x[0]
                x_jarak = int(x[1]*1000) #diubah menjadi satuan meter
                for y in all_data:
                    lat_ke_y = float(y.latitude)
                    long_ke_y = float(y.longitude)
                    data_jarak = (lat_ke_y, long_ke_y)
                    if data_jarak == x_tetangga:
                        data_terdekat.append((y, x_jarak))

    context = {
        'datas': datas,
        'cari': cari,
        'riwayats': all_riwayat,
        'data_terdekat': data_terdekat,
        'all_data': all_data,
        'data_favorite': data_favorite,
    }

    return render(request, 'skripsi/Search.html', context)


def delete_riwayat(request, riwayat_id):
    riwayat = Riwayat.objects.get(pk=riwayat_id)
    riwayat.delete()
    
    return redirect('search')

def favorite(request, favorite_id):
    
    coffee_shop_id = favorite_id

    try:
        favorite = Favorite.objects.get(coffee_shop_id=coffee_shop_id)
        favorite.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create(coffee_shop_id=coffee_shop_id)
        
    return redirect('search')

        
def delete_favorite(request):
    Favorite.objects.all().delete()
    
    return redirect('search')

def detail(request, id):
        
    coffee_shop = get_object_or_404(CoffeeShop, pk=id)

    all_data = CoffeeShop.objects.all()
    
    datas = sample(list(all_data), min(6, len(all_data)))

    from_search = request.GET.get('from_search')
    if from_search:
        Riwayat.objects.create(coffee_shop=coffee_shop)

    
    # mapping data profile
    mapping_data_profile = []
    field_to_map = ['harga_makanan','harga_minuman','wifi', 'mushola', 'ruang_lesehan', 'ruang_ac', 'halaman_parkir', 'live_music', 'hiburan', 'kabel_terminal', 'toilet']
    
    for i in field_to_map :
        field_value = getattr(coffee_shop, i)
        if field_value == "Ya" :
            mapping_data_profile.append(1)
        elif field_value == "Tidak" :
            mapping_data_profile.append(0)
        elif 1000 < field_value <= 10000 :
            mapping_data_profile.append(1)
        elif 10000 < field_value <= 15000 :
            mapping_data_profile.append(2)
        elif 15000 < field_value <= 20000 :
            mapping_data_profile.append(3)
        elif 20000 < field_value <= 25000 :
            mapping_data_profile.append(4)
        elif 25000 < field_value <= 30000:
            mapping_data_profile.append(5)
        elif 30000 < field_value <= 35000 :
            mapping_data_profile.append(6)
        elif field_value > 35000 :
            mapping_data_profile.append(7)
        else :
            mapping_data_profile.append(field_value)
    
    
    # mapping dataset
    mapping_dataset = []
    
    for i in all_data:
        temp = []
        for j in CoffeeShop._meta.fields:
            field_value_j = getattr(i,j.name)
            if field_value_j == "Ya":
                temp.append(1)
            elif field_value_j == "Tidak":
                temp.append(0)
            elif isinstance(field_value_j, int):
                if 1000 < field_value_j <= 10000 :
                    temp.append(1)
                elif 10000 < field_value_j <= 15000 :
                    temp.append(2)
                elif 15000 < field_value_j <= 20000 :
                    temp.append(3)
                elif 20000 < field_value_j <= 25000 :
                    temp.append(4)
                elif 25000 < field_value_j <= 30000:
                    temp.append(5)
                elif 30000 < field_value_j <= 35000 :
                    temp.append(6)
                elif field_value_j > 35000 :
                    temp.append(7)
                else:
                    temp.append(field_value_j)
            else :
                temp.append(field_value_j)
            
        mapping_dataset.append(temp)
    
    # mengambil atribut nama_cafe, harga_makanan, harga_minuman, dan fasilitas yang dimiliki oleh cafe (wifi, live music, dll)
    dataset = []
    for i in mapping_dataset:
        temp1 = i[1]
        temp2 = i[3:5] + i[7:16]
        dataset.append((temp1,temp2))
    
    # menghitung kesamaan menggunakan cosine similarity
    similarity = []
    for i in dataset :
        temp = cosine_similarity(mapping_data_profile, i[1])
        nama_cafe = i[0]
        similarity.append((nama_cafe,temp))
    
    # mengurutkan data berdasarkan hasil yang mendekati 1
    sorted_similarity = sorted(similarity, key=lambda x:x[1], reverse=True)
    rekomend = sorted_similarity[1:21] # mengambil 20 data yang memiliki nilai tertinggi
    
    print()
    print("Rekomendasi Coffee Shop")
    for i in rekomend :
        print(i)
    print()
    
    # berfungsi agar rekomendasi bisa di akses di html
    rekomendasi = []
    for x in rekomend :
        similar = x[1]
        for y in all_data :
            data = y.nama
            if x[0] == data:
                rekomendasi.append((y,similar))

    
    # Mengambil kolom nama cafe
    data_user = Favorite.objects.values_list('coffee_shop_id', flat=True)
    favorite_user = CoffeeShop.objects.filter(id__in=data_user).values_list('nama', flat=True)
    print("Coffee Shop yang disuka oleh user :")
    for i, x in enumerate(favorite_user, start=1) :
        print(f"{i}. {x}")
    
    data1 = CoffeeShop.objects.values_list('nama', flat=True)
    # contoh data coffee shop yang direkomendasikan oleh sistem sebanyak 6
    hasil_rekomendasi = [x[0] for x in rekomend]

    tp = fp = fn = 0
    print()
    for x in data1 :
        if x in favorite_user and x in hasil_rekomendasi :
            tp += 1
        elif x not in favorite_user and x in hasil_rekomendasi :
            fp += 1 
        elif x in favorite_user and x not in hasil_rekomendasi :
            fn += 1 
    
    recall_user = []
    precision_user = []
    temp1 = 0
    temp2 = 1
    
    print("Nilai Recall dan Precision pada setiap rekomendasi oleh pengguna :\n")
    for x in hasil_rekomendasi :
        if x in favorite_user :
            print("Yang disukai user dan direkomendasikan")
            temp1 += 1
            precision_x = temp1/temp2
            recall_x = temp1/tp
            recall_user.append(recall_x)
            precision_user.append(precision_x)
        
        temp_recall = temp1/tp
        temp_precision = temp1/temp2
        
        temp2 += 1
        
        print(x,' memiliki recall : ',temp_recall)
        print(x,' memiliki precision : ',temp_precision)
        print()
    
    print()
    print ("True Posistive:", tp) # Jumlah coffee shop yang disukai user dan sistem merekomendasikan
    print ("False Positive:", fp) # Jumlah coffee shop yang tidak disukai user tapi sistem merekomendasikan
    print ("False Negative:", fn) # Jumlah coffee shop yang disukai user tetapi sistem tidak merekomendasikan
    print()
    
    if precision_user is not None and precision_user :
        avg_recall = sum(recall_user)/len(favorite_user)
        avg_precision = sum(precision_user)/temp1
        print("Hasil Perfoma Sistem")
        print("Rata-rata Recall:", avg_recall)
        print("Rata-rata Precision:", avg_precision)
        print()
    
    context = {
        'coffee_shop': coffee_shop,
        'datas': datas,
        'rekomendasi': rekomendasi
    }

    return render(request, 'skripsi/Detail.html', context)


# function menghitung jarak antara dataset dengan data profile
def haversine(row1, row2):
    lat1, long1 = row1
    lat2, long2 = row2

    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    dlat = lat2 - lat1
    dlong = long2 - long1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    radius_bumi_km = 6371.0

    distance = radius_bumi_km * c

    return distance

# function mencari tetangga terdekat
def get_neighbors(train, test_row, k):
    distances = []
    #menghitung tiap jarak antara data test dengan masing-masing data train
    for train_row in train:
        dist = haversine(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = [(tup[0], tup[1]) for tup in distances[:k]]
    return neighbors

# function menghitung kesamaan kontent menggunakan cosine similarity
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2) # menghitung tiap konten antara vektor1 dan vektor2
    norm1 = np.linalg.norm(vector1) #menghitung akar dari jumlah kuadrat pada vektor1
    norm2 = np.linalg.norm(vector2) #menghitung akar dari jumlah kuadrat pada vektor2
    cosine_similarity = dot_product / (norm1 * norm2)
    return cosine_similarity