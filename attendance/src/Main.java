import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Work work = new Work();
        while (work.getProcess() == 1) {
            System.out.println("1. 학생 추가");
            System.out.println("2. 모든 학생 조회");
            System.out.println("3. 학생 파트 수정");
            System.out.println("4. 학생 삭제");
            System.out.println("5. BACKEND 파트 학생 필터링");
            System.out.println("6. 평균 기수 계산");
            System.out.println("7. 종료");
            System.out.print("원하는 작업을 선택하세요: ");

            Scanner scanner = new Scanner(System.in);
            int choice = scanner.nextInt();
            work.setChoice(choice);
            work.work();
        }
    }
}
