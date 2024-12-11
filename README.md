# Reusable Workflows

**Reusable Workflows** must be in the `.github/workflows`
좋은 지적입니다! 다른 레포지토리에서 이 reusable workflow를 호출할 때 상대 경로로 지정된 custom actions은 문제가 될 수 있습니다.

상세히 설명드리면:

1. 다른 레포지토리에서 workflow를 호출할 때, 상대 경로 (`./`)로 된 actions은 호출하는 레포지토리의 컨텍스트에서 찾기 때문에 실행되지 않을 수 있습니다.

2. 이런 경우 해결 방법은 두 가지입니다:
   - Fully qualified된 actions 경로 사용 (레포지토리 전체 경로)
   - Custom actions를 별도의 레포지토리로 분리

예시:
```yaml
# 문제가 될 수 있는 코드 (상대 경로)
uses: ./.github/actions/my-custom-action

# 권장되는 방식 (절대 경로)
uses: owner/repo/.github/actions/my-custom-action@v1
```

따라서 다른 레포에서 재사용하려면 custom actions의 경로를 명시적으로 지정해야 합니다.