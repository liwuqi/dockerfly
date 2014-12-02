简介:
========================
长期项目，基于docker，为快速建立开发/测试环境，一键部署，自动化测试提供基础接口，并在此基础上构建工具集


参考资料:
-------------------------------------

docker:

    https://docs.docker.com/

中文文档:

    http://yeasy.gitbooks.io/docker_practice/content/index.html

网络:

    采用macvtap虚拟网卡，用nsent 添加到container的namespace中，IP从IP池中依次分配
