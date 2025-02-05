# Müzik İndirme Uygulaması 🎵

Bu proje, YouTube bağlantılarından müzik indirmenizi sağlayan bir Python uygulamasıdır. Kullanıcı dostu bir arayüze sahip olup, indirme öncesinde şarkı bilgilerini gösterir ve ilerleme durumunu takip etmenizi sağlar.

## 🚀 Özellikler
- **YouTube desteği**: YouTube bağlantılarından müzik indirebilir.
- **Şarkı bilgilerini önceden görüntüleme**: İndirme başlamadan önce şarkının adı ve diğer detaylar gösterilir.
- **İlerleme çubuğu & kalan süre**: İndirme işlemi sırasında süreci takip edebilirsiniz.
- **FFmpeg entegrasyonu**: Ses dönüştürme işlemleri için otomatik FFmpeg kullanımı.
- **Kayıt yeri seçme**: Kullanıcı, indirme tamamlandıktan sonra dosyanın kaydedileceği konumu seçebilir.
- **Bağlantı desteği**: Sadece YouTube bağlantılarını destekler, diğer linklerde uyarı verir.

## 🛠️ Gereksinimler
Bu projeyi çalıştırmak için aşağıdaki bağımlılıkların yüklü olması gerekmektedir:

```bash
pip install -r requirements.txt
```

Bağımlılıklar:
- Python 3.x
- PyQt6
- yt-dlp
- FFmpeg

## 📥 Kurulum ve Kullanım

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/kullanici/muzik-indirici.git
cd muzik-indirici
```
2. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```
3. **Uygulamayı başlatın:**
```bash
python main.py
```

## 📌 Notlar
- Eğer FFmpeg eksikse, uygulama otomatik olarak indirmeye çalışacaktır.
- İndirilen müzik dosyaları `downloads/` klasörüne kaydedilecektir.
- YouTube dışındaki bağlantılar desteklenmez ve hata mesajı verir.

## 📜 Lisans
Bu proje açık kaynaklıdır ve [MIT Lisansı](LICENSE) ile lisanslanmıştır.
