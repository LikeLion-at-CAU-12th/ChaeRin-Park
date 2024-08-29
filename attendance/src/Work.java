import java.util.Optional;
import java.util.Scanner;

public class Work {
    private int choice;
    private MemberList memberlist;
    private int process;

    public Work() {
        this.process = 1;
        this.memberlist = new MemberList();
    }

    public int getProcess() {
        return process;
    }

    public void setChoice(int choice) {
        this.choice = choice;
    }

    public void work() {
        Scanner scanner = new Scanner(System.in);

        // 1. 학생 추가
        if (choice == 1) {
            System.out.print("추가할 학생의 이름을 입력해주세요: ");
            String name = scanner.next();

            System.out.print("추가할 학생의 기수를 입력해주세요: ");
            int generation = scanner.nextInt();

            System.out.print("추가할 학생의 파트를 입력해주세요: ");
            String input = scanner.next().toUpperCase();
            Part part = null;
            try {
                part = Part.valueOf(input); // 문자열을 Enum으로 변환
            } catch (IllegalArgumentException e) {
                System.out.println("올바르지 않은 값입니다.");
            }

            Member member = new Member(name, generation, part);
            memberlist.addMember(member);
        }

        // 2. 모든 학생 조회
        else if (choice == 2) {
            memberlist.readMemberList();
        }

        // 3. 학생 파트 수정
        else if (choice == 3) {
            System.out.print("수정할 학생의 이름을 입력해주세요: ");
            String name = scanner.next();
            System.out.print("수정할 파트를 입력해주세요: ");
            String input = scanner.next().toUpperCase();
            Part part = null;
            try {
                part = Part.valueOf(input); // 문자열을 Enum으로 변환
                memberlist.updateMember(name, Optional.empty(), Optional.empty(), Optional.of(part));
                System.out.println("수정되었습니다.");
            } catch (IllegalArgumentException e) {
                System.out.println("올바르지 않은 값입니다.");
            }
        }

        // 4. 학생 삭제
        else if (choice == 4) {
            System.out.print("삭제할 학생의 이름을 입력해주세요: ");
            String name = scanner.next();
            memberlist.deleteMember(name);
            System.out.println("삭제되었습니다.");
        }

        // 5. 백엔드 학생 필터링
        else if (choice == 5) {
            memberlist.printBackend();
        }

        // 6. 평균 기수 계산
        else if (choice == 6) {
            memberlist.generationAverage();
        }

        // 7. 종료
        else if (choice == 7) {
            scanner.close();
            process = 0;
        }
    }
}
