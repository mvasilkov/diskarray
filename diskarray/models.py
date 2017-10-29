from datetime import datetime

from django.db import models


class Disk(models.Model):
    dev_name = models.CharField(max_length=20)
    mount_point = models.CharField(max_length=40)
    is_healthy = models.BooleanField()

    def __str__(self):
        return '%s on %s' % (self.dev_name, self.mount_point)


class File(models.Model):
    vpath = models.CharField(max_length=1000)
    sha256 = models.CharField(max_length=64, unique=True)
    storage_class = models.PositiveSmallIntegerField(default=1)
    gen = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.vpath


class FileCopy(models.Model):
    NEVER = datetime(1970, 1, 1)

    disk = models.ForeignKey(Disk, on_delete=models.PROTECT)
    file = models.ForeignKey(File, on_delete=models.PROTECT, related_name='copies')
    path = models.CharField(max_length=1000)
    is_healthy = models.BooleanField()
    last_checked = models.DateTimeField(default=NEVER)

    class Meta:
        unique_together = ('disk', 'file')
        verbose_name_plural = 'file copies'

    def __str__(self):
        return '(%s) %s' % (self.disk, self.path)


class Oplog(models.Model):
    WAITING = 'waiting'
    WORKING = 'working'
    ENDED = 'ended'
    STAGES = (WAITING, WAITING), (WORKING, WORKING), (ENDED, ENDED)

    command = models.CharField(max_length=1000)
    stage = models.CharField(max_length=10, choices=STAGES, default=WAITING)
    error_code = models.SmallIntegerField(default=-1)
    stdout = models.TextField()
    stderr = models.TextField()

    def __str__(self):
        return '(%s) %s' % (self.stage, self.command)