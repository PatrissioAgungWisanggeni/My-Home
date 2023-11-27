from django.db import models

# Create your models here.
    
class CoffeeShop(models.Model):
    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    harga_makanan = models.IntegerField()
    harga_minuman = models.IntegerField()
    deskripsi = models.TextField()
    gambar = models.BinaryField(null=True, blank=True)
    wifi = models.CharField(max_length=5, null=True)
    mushola = models.CharField(max_length=5, null=True)
    ruang_lesehan = models.CharField(max_length=5, null=True)
    ruang_ac = models.CharField(max_length=5, null=True)
    halaman_parkir = models.CharField(max_length=5, null=True)
    live_music = models.CharField(max_length=5, null=True)
    hiburan = models.CharField(max_length=5, null=True)
    kabel_terminal = models.CharField(max_length=6, null=True)
    toilet = models.CharField(max_length=5, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=6, null=True)

    def __str__(self):
        return self.nama
    
class Riwayat(models.Model):
    coffee_shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    waktu_pemilihan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coffee_shop.nama
    
class Favorite(models.Model):
    coffee_shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    waktu_pemilihan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coffee_shop.nama