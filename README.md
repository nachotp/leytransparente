# ley Transparente

## Ejecutar

Servidor
```shell
python manage.py runserver
```

Servidor dummy de correos (según corresponda el OS)
```shell
smtpd.bat/.sh
```

## MongoDB Atlas

```python
client = pymongo.MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites=true&w=majority")
```
## Embeddings

*Word embeddings* de palabras en español [1] computados con [fastText](https://github.com/facebookresearch/fastText). Hay tres archivos de distintos tamaños. Actualmente usando el 855K

- 100K vectores (94 MB): [http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.100k.vec.gz](http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.100k.vec.gz)
- 300K vectores (281 MB): [http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.300k.vec.gz](http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.300k.vec.gz)
- *855K vectores (801 MB)*: [http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.vec.gz](http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.vec.gz)

# The End