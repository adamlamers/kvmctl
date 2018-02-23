import click
import collections

def recursive_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = recursive_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def recursive_walk(dictionary, callback=None, parents=[]):

    for key, val in dictionary.items():
        if isinstance(val, dict):
            parents.append(key)
            recursive_walk(val, callback=callback, parents=parents)
            parents.pop()
        else:
            if callable(callback):
                callback(parents + [key], val)

@click.group(name='configure', invoke_without_command=True)
@click.pass_context
def this(ctx):
    config = ctx.obj['CONFIG'].data

    def configure_item(parents, old_val):

        val = click.prompt('.'.join(parents), old_val)

        d = {}
        top = d
        for idx, parent in enumerate(parents):
            if idx != len(parents)-1:
                d[parent] = {}
                d = d[parent]
            else:
                d[parent] = val

        recursive_update(config, top)

    recursive_walk(config, callback=configure_item)

    ctx.obj['CONFIG'].save(config)
