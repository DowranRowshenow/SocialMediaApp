function CopyClipboard(element) 
{
    element.select();
    element.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(element.value);
}