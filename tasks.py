from invoke import task

@task
def init(ctx):
    ctx.run("terraform init -backend-config $CIRCLE_WORKING_DIRECTORY/backend.conf")

@task
def output(ctx):
    ctx.run("terraform output -json -module cluster_vpc k8_cluster_name > k8_cluster_name.json")
    ctx.run("terraform output -json -module cluster_vpc public_subnet_objects > public_subnet_objects.json")
    ctx.run("terraform output -json -module cluster_vpc nat_subnet_objects > nat_subnet_objects.json")
    ctx.run("terraform output -json -module cluster_vpc vpc > vpc.json")
    ctx.run("terraform output -json -module cluster_vpc natgw_ids  > natgateway.json")


@task
def enc(ctx, file='local.env', encoded_file='env.ci'):
    ctx.run("openssl aes-256-cbc -e -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(file, encoded_file))

@task
def dec(ctx, encoded_file='env.ci', file='local.env'):
    ctx.run("openssl aes-256-cbc -d -in {} -out {} -k $FEEDYARD_PIPELINE_KEY".format(encoded_file, file))