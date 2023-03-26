from prefect.filesystems import GitHub

# alternative to creating GitHub block in the UI

gh_block = GitHub(
    name="ecommerce_behavior", repository="https://github.com/fluentnumbers/ecommerce_behavior"
)

gh_block.save("ecommerce_behavior", overwrite=True)
