#! /usr/bin/python3
import kubernetes
from kubernetes import client, config
from kubernetes.config.kube_config import KubeConfigLoader
import re, os
from pprint import pprint

def main():    

    
    config.load_kube_config()
    client=kubernetes.client.ApiClient()
    coreV1Api = kubernetes.client.CoreV1Api(client)
    networkApi = kubernetes.client.ExtensionsV1beta1Api(client)
    appsV1Api = kubernetes.client.AppsV1Api(client)


    host = "yb.ingress"

    # master ingress
    masteringress = 'yb-master-ingress'
    if existsIngress(networkApi, 'default', masteringress) == False:            
        createIngressMaster(networkApi, masteringress, host)

    namespaces = ['pr-12345', 'pr-12346']

    name = 'demo-server'
    for ns in namespaces:
        if existsNamespace(coreV1Api, ns) == False:        
            createNamespace(coreV1Api, ns)

        if existsIngress(networkApi, ns, ns) == False:
            createIngressPR(networkApi, ns, name, host)        
        
        if existsService(coreV1Api, ns, name) == False:        
            createService(coreV1Api, ns, name)    
                
        image = 'docker-registry.yourbase.io/demo-server:latest'
        if existsDeployment(appsV1Api, ns, name) == False:
            createDeployment(appsV1Api, ns, name, image)

def existsDeployment(appsApi, namespace, name):    
    field_selector = 'metadata.name=%s,metadata.namespace=%s' % (name, namespace)
    res = appsApi.list_deployment_for_all_namespaces(field_selector=field_selector)    
    if len(res.items) == 0:
         return False

    return True

def createDeployment(appsApi, namespace, name, image):    
    container = client.V1Container(
        name=name,
        image=image,
        image_pull_policy="Always",
        ports=[client.V1ContainerPort(container_port=3001)]
    )
        
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container]))
    networkApi = client.ExtensionsV1beta1Api()
    selector = client.V1LabelSelector(
        match_labels={"app":name}
    )
    
    spec = client.V1DeploymentSpec(
        replicas=1,        
        template=template,
        selector={'matchLabels': {'app': name}})
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)
    
    appsApi.create_namespaced_deployment(
        namespace=namespace, body=deployment
    )

def existsNamespace(coreApi, namespace):        
    field_selector = 'metadata.name='+namespace
    res = coreApi.list_namespace(field_selector=field_selector)
    if len(res.items) == 0:
        return False

    return True

def createNamespace(coreApi, namespace):        
    body = client.V1Namespace(
        api_version="v1",
        kind="Namespace",
        metadata=client.V1ObjectMeta(
            name=namespace
        )
    )

    coreApi.create_namespace(body)

def existsService(coreApi, namespace, servicename):    
    namespace_field_selector = 'metadata.namespace='+namespace
    name_field_selector = 'metadata.name='+servicename
    res = coreApi.list_service_for_all_namespaces(field_selector=name_field_selector+","+ namespace_field_selector)    
    if len(res.items) == 0:
        return False

    return True

def createService(coreApi, namespace, name):        
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=name,
        ),
        spec=client.V1ServiceSpec(
            selector={"app": name},
            ports=[client.V1ServicePort(
                port=8086,
                target_port=3001
            )]
        ),        
    )

    coreApi.create_namespaced_service(namespace=namespace, body=body)

def existsIngress(networkApi, namespace, name):       
    field_selector = 'metadata.name=%s,metadata.namespace=%s' % (name, namespace)
    res = networkApi.list_ingress_for_all_namespaces(field_selector=field_selector)        
    if len(res.items) == 0:
         return False

    return True
 
def createIngressPR(networkApi, namespace, name, host):    
    body = client.ExtensionsV1beta1Ingress(
        api_version="extensions/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(
            name=namespace,
            namespace=namespace,
            annotations={                
                "kubernetes.io/ingress.class": "nginx",
                "nginx.org/mergeable-ingress-type": "minion",
                "nginx.ingress.kubernetes.io/rewrite-target": "/$1"
            }),
        spec=client.NetworkingV1beta1IngressSpec(
            rules=[client.NetworkingV1beta1IngressRule(
                host=host,
                http=client.NetworkingV1beta1HTTPIngressRuleValue(
                    paths=[client.NetworkingV1beta1HTTPIngressPath(
                        path="/"+namespace+"/(.*)",
                        backend=client.NetworkingV1beta1IngressBackend(
                            service_port=8086,
                            service_name=name)

                    )]
                )
            )]
        )
    )
    
    networkApi.create_namespaced_ingress(
        namespace=namespace,
        body=body
    )

def createIngressMaster(networkApi, name, host):         
    body = client.ExtensionsV1beta1Ingress(
        api_version="extensions/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(
            name=name,
            annotations={                
                "kubernetes.io/ingress.class": "nginx",
                "nginx.org/mergeable-ingress-type": "master",                       
            }),
        spec=client.NetworkingV1beta1IngressSpec(
            rules=[client.NetworkingV1beta1IngressRule(
                host=host)
            ])
    )
    
    networkApi.create_namespaced_ingress(
        namespace="default",
        body=body
    )

if __name__=="__main__":
   main()
    