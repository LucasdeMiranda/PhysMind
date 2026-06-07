#!/usr/bin/env python
"""
Script para executar todos os testes do projeto
Executa testes de backend (Django) e frontend (Flutter)
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Cores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def run_django_tests():
    """Executar testes do Django"""
    print_header("Testes Backend - Django")

    project_root = Path(__file__).parent
    os.chdir(str(project_root))

    # Verificar se manage.py existe
    if not Path('manage.py').exists():
        print_error("manage.py não encontrado")
        return False

    print_info("Preparando banco de dados para testes...")

    tests_to_run = [
        {
            'name': 'Testes de Autenticação e Login',
            'module': 'test_api_complete.UsuarioAuthTestCase',
            'description': 'Login, cadastro e obtenção de tokens JWT'
        },
        {
            'name': 'Testes de Alimentos e Dieta',
            'module': 'test_api_complete.AlimentoDietaTestCase',
            'description': 'Inserção e deleção de alimentos'
        },
        {
            'name': 'Fluxo Completo',
            'module': 'test_api_complete.FluxoCompletoTestCase',
            'description': 'Login → Inserir → Deletar'
        },
        {
            'name': 'Testes de Integração Flutter',
            'module': 'test_flutter_integration.FlutterMobileIntegrationTestCase',
            'description': 'Simulação de requisições do Flutter'
        },
    ]

    all_passed = True
    results = []

    for test_config in tests_to_run:
        print(f"\n{Colors.BOLD}Executando: {test_config['name']}{Colors.ENDC}")
        print(f"  {test_config['description']}")
        print(f"  {'-'*50}")

        cmd = [
            sys.executable, 'manage.py', 'test',
            test_config['module'],
            '--verbosity=2'
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print_success(f"{test_config['name']} passou")
                results.append({
                    'test': test_config['name'],
                    'status': 'PASSOU',
                    'output': result.stdout
                })
            else:
                print_error(f"{test_config['name']} falhou")
                print(result.stdout)
                print(result.stderr)
                results.append({
                    'test': test_config['name'],
                    'status': 'FALHOU',
                    'output': result.stdout + result.stderr
                })
                all_passed = False

        except subprocess.TimeoutExpired:
            print_error(f"{test_config['name']} expirou")
            results.append({
                'test': test_config['name'],
                'status': 'TIMEOUT',
                'output': ''
            })
            all_passed = False
        except Exception as e:
            print_error(f"Erro ao executar {test_config['name']}: {str(e)}")
            results.append({
                'test': test_config['name'],
                'status': 'ERRO',
                'output': str(e)
            })
            all_passed = False

    return all_passed, results


def run_flutter_tests():
    """Executar testes do Flutter"""
    print_header("Testes Frontend - Flutter")

    project_root = Path(__file__).parent / 'mobile'

    if not project_root.exists():
        print_warning("Diretório mobile não encontrado, pulando testes Flutter")
        return True, []

    os.chdir(str(project_root))

    # Verificar se pubspec.yaml existe
    if not Path('pubspec.yaml').exists():
        print_warning("pubspec.yaml não encontrado, pulando testes Flutter")
        return True, []

    print_info("Executando testes Flutter com flutter test...")

    cmd = ['flutter', 'test', 'test/test_complete_flow.dart', '-v']

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print_success("Testes Flutter passaram")
            return True, [{'test': 'Flutter Tests', 'status': 'PASSOU'}]
        else:
            print_warning("Testes Flutter com avisos ou falhas")
            print(result.stdout)
            return False, [{'test': 'Flutter Tests', 'status': 'FALHOU'}]

    except FileNotFoundError:
        print_warning("Flutter CLI não encontrado. Instale Flutter para executar esses testes.")
        return True, []
    except subprocess.TimeoutExpired:
        print_error("Testes Flutter expiraram")
        return False, [{'test': 'Flutter Tests', 'status': 'TIMEOUT'}]
    except Exception as e:
        print_error(f"Erro ao executar testes Flutter: {str(e)}")
        return False, [{'test': 'Flutter Tests', 'status': 'ERRO'}]


def generate_test_report(django_results, flutter_results):
    """Gerar relatório final dos testes"""
    print_header("Relatório Final dos Testes")

    total_tests = len(django_results) + len(flutter_results)
    passed_tests = sum(1 for r in django_results + flutter_results if r['status'] == 'PASSOU')
    failed_tests = total_tests - passed_tests

    print(f"{Colors.BOLD}Resumo:{Colors.ENDC}")
    print(f"  Total de suites de testes: {total_tests}")
    print(f"  {Colors.OKGREEN}Passou: {passed_tests}{Colors.ENDC}")
    if failed_tests > 0:
        print(f"  {Colors.FAIL}Falhou: {failed_tests}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Detalhes:{Colors.ENDC}")

    all_results = [
        ('Backend - Django', django_results),
        ('Frontend - Flutter', flutter_results),
    ]

    for section_name, results in all_results:
        if results:
            print(f"\n  {section_name}:")
            for result in results:
                status_str = '✓' if result['status'] == 'PASSOU' else '✗'
                status_color = Colors.OKGREEN if result['status'] == 'PASSOU' else Colors.FAIL
                print(f"    {status_color}{status_str} {result['test']}: {result['status']}{Colors.ENDC}")

    # Salvar relatório em JSON
    report = {
        'total_tests': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'backend': django_results,
        'frontend': flutter_results,
    }

    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n{Colors.OKBLUE}Relatório salvo em: test_report.json{Colors.ENDC}")

    return failed_tests == 0


def main():
    """Função principal"""
    print_header("Testes Automatizados - PhysMind")

    print_info("Iniciando testes do fluxo completo...")
    print_info("Backend: Django Rest Framework")
    print_info("Frontend: Flutter")
    print_info("Banco de Dados: SQLite")

    # Executar testes Django
    django_passed, django_results = run_django_tests()

    # Executar testes Flutter
    flutter_passed, flutter_results = run_flutter_tests()

    # Gerar relatório
    all_passed = generate_test_report(django_results, flutter_results)

    # Retornar código de saída
    if all_passed:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}Todos os testes passaram! ✓{Colors.ENDC}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}Alguns testes falharam! ✗{Colors.ENDC}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
