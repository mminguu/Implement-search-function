
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from chat.models import Policy

class Command(BaseCommand):
    help = 'Load policy data from JSON file'

    def handle(self, *args, **kwargs):
        # JSON 파일 경로 설정
        # settings.BASE_DIR이 django_app/config 라고 가정
        # 실제 데이터 위치: project_root/data/processed/...
        
        # /Users/kangminji/검색기능구현/django_app/config
        base_dir = settings.BASE_DIR
        
        # /Users/kangminji/검색기능구현
        # django_app/config -> parent -> django_app -> parent -> project_root
        project_root = base_dir.parent.parent
        
        json_path = os.path.join(project_root, 'data', 'processed', '2026_youth_policies_filtered_kr_revised.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            # Fallback handling just in case BASE_DIR is different
            json_path = '/Users/kangminji/검색기능구현/data/processed/2026_youth_policies_filtered_kr_revised.json'
            if not os.path.exists(json_path):
                self.stdout.write(self.style.ERROR(f'File really not found: {json_path}'))
                return

        self.stdout.write(f'Loading data from {json_path}...')

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.stdout.write(f'Found {len(data)} policies. Starting import...')

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            # 기존 데이터 삭제 옵션을 줄 수도 있지만, 여기서는 중복 방지 로직(get_or_create) 또는 단순 추가로 진행
            # 정책명이 유니크하지 않을 수 있으므로, 내용 기반 혹은 그냥 모두 추가하되 기존것을 지우고 다시 넣는게 깔끔할 수 있음
            # 사용자 요청: "DB에 저장하는 로직" -> 단순 추가?
            # 보통 이런 데이터 로딩은 초기화 후 적재가 일반적이나, 안전하게 기존 데이터 유지하며 추가/업데이트 하겠음.
            # 하지만 고유 ID가 JSON에 없으므로 (정책명 + 기관명) 등으로 식별하거나,
            # 그냥 간단하게 이번 실행에서는 기존 데이터 모두 삭제하고 새로 적재하는 방식 선택 (clean sweep)
            
            Policy.objects.all().delete()
            self.stdout.write('Deleted existing policies.')

            for item in data:
                try:
                    # 숫자 필드 변환
                    def parse_int(val):
                        if not val: return 0
                        try:
                            return int(float(val)) # "0" or "0.0"
                        except:
                            return 0

                    policy = Policy(
                        title=item.get("정책명", ""),
                        keywords=item.get("정책키워드", ""),
                        description=item.get("정책설명", ""),
                        category_major=item.get("대분류", ""),
                        category_middle=item.get("중분류", ""),
                        support_content=item.get("지원내용", ""),
                        min_support_amount=item.get("최소지원금액", ""),
                        max_support_amount=item.get("최대지원금액", ""),
                        age_min=parse_int(item.get("지원최소연령")),
                        age_max=parse_int(item.get("지원최대연령")),
                        hosting_org=item.get("주관기관명", ""),
                        registering_org=item.get("등록기관명", ""),
                        parent_org=item.get("상위기관명", ""),
                        parent_registering_org=item.get("상위등록기관명", ""),
                        application_period=item.get("신청기간", ""),
                        application_method=item.get("신청방법", ""),
                        required_documents=item.get("제출서류", ""),
                        start_date=item.get("사업시작일", ""),
                        end_date=item.get("사업종료일", ""),
                        selection_method=item.get("선정방법", ""),
                        ref_url1=item.get("참고URL1", ""),
                        ref_url2=item.get("참고URL2", ""),
                        app_url=item.get("신청URL", ""),
                        provider_group=item.get("재공기관그룹", ""),
                        provision_method=item.get("정책제공방법", ""),
                        approval_status=item.get("정책승인상태", ""),
                        period_type=item.get("신청기간구분", ""),
                        period_type_biz=item.get("사업기간구분", ""),
                        marital_status=item.get("혼인상태", ""),
                        income_condition=item.get("소득조건", ""),
                        major_requirement=item.get("전공요건", ""),
                        employment_status=item.get("취업상태", ""),
                        education_requirement=item.get("학력요건", ""),
                        specialization=item.get("특화분야", ""),
                        region=item.get("지역", ""),
                        region_scope=item.get("지역범위", ""),
                        additional_condition=item.get("추가자격조건", ""),
                        exclusion_criteria=item.get("참여제외대상", ""),
                        operating_org=item.get("운영기관명", ""),
                        other_support_condition=item.get("기타지원조건", "")
                    )
                    policy.save()
                    created_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error saving policy {item.get("정책명")}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} policies.'))
