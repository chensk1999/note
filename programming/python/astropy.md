```python
from astropy.io import fits

# 打开fits文件
hdul = fits.open('test.fits')
    # hdul(header data unit list)是一个类似list的对象，装有所有的hdu
    # hdul[0]是primary HDU，其他的（如果有）是extension HDU

# 查看各个hdu的信息
hdul.info()
hdu = hdul[0]

# 查看header
hdu.header['NAXIS1']
hdu.header.comments['NAXIS1']

# 读取数据（np.ndarray对象）
data = hdu.data

# 关闭
hdul.close()
```

