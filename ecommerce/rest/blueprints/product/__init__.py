from blueprints import db
from flask_restful import fields
import datetime

class Products(db.Model):

    tablename = "products"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    merk = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    posted_at = db.Column(db.String(255), nullable=False)    
    posted_by = db.Column(db.String(255), nullable=False)    
    kondisi = db.Column(db.String(10), nullable=False)
    garansi = db.Column(db.String(100), nullable=False)
    processor = db.Column(db.String(255), nullable=False)
    vga = db.Column(db.String(255), nullable=False)
    ram = db.Column(db.String(255), nullable=False)
    storage = db.Column(db.String(255), nullable=False)
    monitor = db.Column(db.String(255), nullable=False)
    kelengkapan = db.Column(db.String(255), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    harga = db.Column(db.Integer, nullable=False)


    response_field = {
        'id' : fields.Integer,
        'merk' : fields.String,
        'type' : fields.String,
        'category' : fields.String,
        'posted_at' : fields.String,
        'posted_by' : fields.String,
        'kondisi' : fields.String,
        'garansi' : fields.String,
        'processor' : fields.String,
        'vga' : fields.String,
        'ram' : fields.String,
        'storage' : fields.String,
        'monitor' : fields.String,
        'kelengkapan' : fields.String,
        'deskripsi' : fields.String,
        'harga' : fields.String,
    }
    def __init__(self, id, merk, type, category, posted_at, posted_by, kondisi, garansi, processor, vga, ram, storage, monitor, kelengkapan, deskripsi, harga):
        
        self.id = id
        self.merk = merk
        self.type = type
        self.category = category
        self.posted_at = posted_at
        self.posted_by = posted_by
        self.kondisi = kondisi
        self.garansi = garansi
        self.processor = processor
        self.vga = vga
        self.ram = ram
        self.storage = storage
        self.monitor = monitor
        self.kelengkapan = kelengkapan
        self.deskripsi = deskripsi
        self.harga = harga

    def __repr__(self):
        return '<Products %r>' % self.id