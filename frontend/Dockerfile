# Używamy tylko serwera Nginx
FROM nginx:alpine

# Kopiujemy gotowe pliki z Twojego komputera (folder dist) do serwera w kontenerze
# Ścieżka dist/frontend wynika z Twoich logów z poprzedniej wiadomości
COPY ./dist/frontend /usr/share/nginx/html

# Otwieramy port
EXPOSE 80

# Uruchamiamy serwer
CMD ["nginx", "-g", "daemon off;"]