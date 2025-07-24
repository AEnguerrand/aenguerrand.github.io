---
author: ["Enguerrand Allamel"]
title: "Securing the Supply Chain: A Practical Guide to SLSA Compliance from Build to Runtime | 保障供应链安全：从构建到运行的SLSA合规实用指南"
date: "2024-08-21"
tags:
  ["kubecon", "cloudnativecon", "security", "software supply chain security"]
---

## Description

Navigating the complexities of supply chain security might seem intimidating, especially with evolving frameworks like SLSA (Supply-chain Levels for Software Artifacts). This beginner-friendly session introduces foundational practices required to secure software from build to runtime using CNCF tools.

In this talk, I explore practical implementations of supply chain security within the Kubernetes ecosystem, covering:

- **Automated build security**: Leveraging GitHub Actions for secure build processes and CI/CD pipelines
- **Keyless artifact signing**: Implementing Cosign for seamless artifact signing without managing keys
- **Runtime policy enforcement**: Using Kyverno for enforcing security policies at runtime
- **Artifact integrity**: Utilizing in-toto and Kubescape to verify and maintain artifact integrity
- **Hardware security**: Integrating Hardware Security Modules (HSMs) for enhanced key management

Key outcomes include actionable insights for achieving SLSA compliance within the CNCF ecosystem and practical strategies to secure your software supply chain from development to production.

Github Repository with lab/examples: [kubecon-cloudnativecon-china-2024-supply-chain-security](https://github.com/AEnguerrand/kubecon-cloudnativecon-china-2024-supply-chain-security)

---

## Key Highlights

### Challenge

- **Supply chain complexity**: Modern software development involves complex dependencies and build processes
- **SLSA framework adoption**: Understanding and implementing SLSA levels can be overwhelming for beginners
- **Tool integration**: Coordinating multiple CNCF tools for comprehensive security coverage
- **Key management**: Balancing security with operational simplicity in artifact signing workflows

### Solution

- **CNCF ecosystem**: Leveraging proven cloud-native tools for end-to-end supply chain security
- **Practical implementation**: Step-by-step guidance for implementing SLSA compliance
- **Keyless signing**: Simplifying artifact signing with Cosign's keyless approach
- **Policy-driven security**: Automated enforcement using Kyverno for runtime protection

### Technologies & Tools

- **GitHub Actions**: Automated build and CI/CD security
- **Cosign**: Keyless container and artifact signing
- **Kyverno**: Kubernetes-native policy management and enforcement
- **in-toto**: Software supply chain integrity framework
- **Kubescape**: Kubernetes security scanning and compliance
- **SLSA Framework**: Supply-chain Levels for Software Artifacts compliance
- **HSMs**: Hardware Security Modules for enhanced key management

---

## Impact & Results

✅ **Beginner-Friendly**: Practical introduction to supply chain security concepts and tools  
✅ **SLSA Compliance**: Clear path to implementing SLSA levels within CNCF ecosystem  
✅ **Hands-on Learning**: Lab exercises and examples for immediate application  
✅ **Tool Integration**: Comprehensive coverage of CNCF security toolchain  
✅ **Production Ready**: Actionable insights for securing real-world software pipelines

---

## Resources

### Conference Presentation

- **Event**: KubeCon + CloudNativeCon + Open Source Summit China 2024
- **Location**: Hong Kong
- **Date**: August 21, 2024

### Video & Materials

{{< youtube 733HXxEnm0I >}}

### Slides & Repository

- [English Slides](https://static.sched.com/hosted_files/kccncossaidevchn2024/91/English%20-%20Securing%20the%20Supply%20Chain%20A%20Practical%20Guide%20to%20SLSA%20Compliance%20from%20Build%20to%20Runtime.pdf)
- [Chinese Slides](https://static.sched.com/hosted_files/kccncossaidevchn2024/3d/Chinese%20%28Automatic%20Translation%29%20-%20Securing%20the%20Supply%20Chain%20A%20Practical%20Guide%20to%20SLSA%20Compliance%20from%20Build%20to%20Runtime.pdf)
- [Lab Repository](https://github.com/AEnguerrand/kubecon-cloudnativecon-china-2024-supply-chain-security)
