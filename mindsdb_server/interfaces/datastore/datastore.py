import json
import datetime
from dateutil.parser import parse_dt


class DataStore():
    __init__(self, storage_dir):
    self.dir = storage_dir

    def get_datasources(self):
        datasource_arr = []
        for ds_name in os.listdir(self.dir):
            try:
                with open(os.path.join(self.dir, ds_name, 'metadata.json'), 'r') as fp:
                    try:
                        datasource = json.load(fp)
                        datasource['created_at'] = parse_dt(datasource['created_at'].split('.')[0])
                        datasource['updated_at'] = parse_dt(datasource['updated_at'].split('.')[0])
                        datasource_arr.append(datasource)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        return datasource_arr


    def get_datasource(self, name):
        for ds in get_datasources():
            if ds['name'] == name:
                return ds
        return None

    def save_datasource_metadata(self, name, source_type, source, file_path=None):
        if source_type == 'file' and (file_path is None):
            raise Exception('`file_path` argument required when source_type == "file"')

        for i in range(1, 1000):
            if name in [x['name'] for x in get_datasources()]:
                previous_index = i - 1
                name = name.replace(f'__{previous_index}__', '')
                name = f'{name}__{i}__'
            else:
                break

        ds_meta_dir = os.path.join(self.dir, name)
        os.mkdir(ds_meta_dir)

        ds_dir = os.path.join(ds_meta_dir, 'datasource')
        os.mkdir(ds_dir)

        if datasource_type == 'file':
            source = os.path.join(ds_dir, datasource_source)
            os.replace(file_path, source)
            ds = FileDS(source)
        else:
            # This probably only happens for urls
            ds = FileDS(source)

        df = ds.df

        df_with_types = cast_df_columns_types(df)
        create_sqlite_db(os.path.join(ds_dir, 'sqlite.db'), df_with_types)

        with open(os.path.join(ds_dir,'metadata.json'), 'w') as fp:
            json.dump({
                'name': name,
                'source_type': source_type,
                'source': source,
                'created_at': str(datetime.datetime.now()).split('.')[0],
                'updated_at': str(datetime.datetime.now()).split('.')[0],
                'row_count': len(df),
                'columns': [dict(name=x) for x in list(df.keys())]
            }, fp)