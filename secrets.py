import os


globals().update(dict(line.strip().split('=')
                      for line in file(os.path.join(
                          'too-many-secrets',
                          'lantern-controller',
                          'org.lantern.secrets.properties'))))
