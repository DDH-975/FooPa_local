 // 결제하기 버튼 클릭 시 실행되는 함수
 function proceedToCheckout() {
    var checkedProducts = document.querySelectorAll('.product-checkbox:checked');
    if (checkedProducts.length === 0) {
        alert("선택된 상품이 없습니다.");
        return;
    }


//뒤로가기 버튼
    function goBack() {
        window.history.back();
      }



    var selectedProductIds = [];
    checkedProducts.forEach(function(checkbox) {
        selectedProductIds.push(checkbox.parentNode.querySelector('h2').textContent);
    });

    // 선택된 상품들의 ID나 다른 정보를 가져와 다음 페이지로 전달
    alert("선택된 상품: " + selectedProductIds.join(", "));



    // 결제 페이지가 들어갈 코드
    // window.location.href = '결제 페이지 URL';
}