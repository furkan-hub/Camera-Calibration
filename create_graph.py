import csv
import matplotlib.pyplot as plt

# CSV dosyasını oku ve mesafeleri listeye ekle
distances = []
with open('distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Başlık satırını atla
    for row in csv_reader:
        distances.append(float(row[0]))

# Mesafeleri grafiğe çiz
plt.figure(figsize=(10, 6))
plt.plot(distances, marker='o', linestyle='-', color='b')
plt.title('Tıklanan İki Nokta Arasındaki Mesafeler')
plt.xlabel('Ölçüm Numarası')
plt.ylabel('Mesafe (mm)')
plt.grid(True)

# Grafiği dosyaya kaydet
plt.savefig('distances_graph.png')

# plt.show() yerine grafiği kaydedin
# plt.show()
print("Grafik 'distances_graph.png' dosyasına kaydedildi.")
